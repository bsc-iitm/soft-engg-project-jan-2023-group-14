# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is Ticket Blueprint file.

# --------------------  Imports  --------------------

import hashlib
import time
from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
from application.common_utils import (
    token_required,
    users_required,
)
from application.views.user_utils import UserUtils
from application.responses import *
from application.models import *
from copy import deepcopy

# --------------------  Code  --------------------


class TicketUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id = user_id

    def convert_ticket_to_dict(self, ticket):
        ticket_dict = vars(ticket)  # verify if this properly converts obj to dict
        if "_sa_instance_state" in ticket_dict:
            del ticket_dict["_sa_instance_state"]
        attachments = self.get_ticket_attachments(ticket_id=ticket.ticket_id)
        ticket_dict["attachments"] = attachments
        print(f"\n\n{ticket_dict}\n\n")
        return ticket_dict

    def get_ticket_attachments(self, ticket_id):
        ticket_attch = TicketAttachment.query.filter_by(ticket_id=ticket_id).all()
        attachments = [
            {"user_id": att.user_id, "attachment_loc": att.attachment_loc}
            for att in ticket_attch
        ]
        return attachments

    def generate_ticket_id(self, title: str, user_id: str) -> str:
        """
        Ticket id is generated from ticket title and user id and timestamp
        """
        # generate unique id
        ts = str(int(time.time_ns()))
        string = f"{user_id}_{title}_{ts}"
        ticket_id = hashlib.md5(string.encode()).hexdigest()
        return ticket_id


ticket_bp = Blueprint("ticket_bp", __name__)
ticket_api = Api(ticket_bp)
ticket_utils = TicketUtils()


class TicketAPI(Resource):
    @token_required
    @users_required(users=["student", "support"])
    def get(self, ticket_id="", user_id=""):
        """
        Usage
        -----
        Get a single ticket for the user and return

        Parameters
        ----------
        ticket is and user id

        Returns
        -------
        Ticket

        """
        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")

        # check if ticket exists and it is created by user_id
        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->get : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket:
                user = Auth.query.filter_by(user_id=user_id).first()
                if user_id == ticket.created_by or user.role == "support":
                    # the ticket and its user are matched or its a support staff
                    # convert to list of dict
                    ticket_dict = ticket_utils.convert_ticket_to_dict(
                        ticket
                    )  # NOT TESTED
                    return success_200_custom(data=ticket_dict)
            else:
                raise NotFoundError(status_msg="Ticket does not exists")

    @token_required
    @users_required(users=["student"])
    def post(self, user_id=""):
        """
        Usage
        -----
        Create a new ticket. Only a student can create.

        Parameters
        ----------
        form data sent with request

        Returns
        -------

        """
        details = {
            "title": "",
            "description": "",
            "priority": "",
            "tag_1": "",
            "tag_2": "",
            "tag_3": "",
        }

        # check user_id
        if ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id is empty/missing in url")

        try:
            user = Auth.query.filter_by(user_id=user_id).first()
            if not user:
                # user id does not exists
                raise NotFoundError(status_msg="User id does not exists.")
        except Exception as e:
            logger.error(
                f"TicketAPI->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError

        # get form data
        try:
            form = request.get_json()
            attachments = form.get("attachments", [])
            for key in details:
                value = form.get(key, "")
                if ticket_utils.is_blank(value):
                    value = ""
                details[key] = value
        except Exception as e:
            logger.error(
                f"TicketAPI->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            if details["title"] == "" or details["tag_1"] == "":
                raise BadRequest(
                    status_msg=f"Ticket title and at least one tag is required"
                )

            ticket_id = ticket_utils.generate_ticket_id(details["title"], user_id)
            details["ticket_id"] = ticket_id
            details["created_by"] = user_id
            details["created_on"] = int(time.time())
            ticket = Ticket(**details)

            try:
                # TODO : How to save attachments is not implemented
                # while creating a ticket a student can upload multiple attachments
                # verify whether each attachment is unique
                _attach = []
                for attach in attachments:
                    if attach["attachment_loc"] in _attach:
                        continue
                    else:
                        _attach.append(attach["attachment_loc"])
                        attach["ticket_id"] = ticket_id
                        ticket_attach = TicketAttachment(**attach)
                        db.session.add(ticket_attach)
                db.session.commit()
            except Exception as e:
                logger.error(
                    f"TicketAPI->post : Error occured while creating a Ticket Attachment : {e}"
                )
                # TODO: db rollback not added yet
                raise InternalServerError(
                    status_msg="Error occured while creating a Ticket Attachment"
                )

            try:
                db.session.add(ticket)
                db.session.commit()
            except Exception as e:
                logger.error(
                    f"TicketAPI->post : Error occured while creating a new ticket : {e}"
                )
                # TODO: db rollback not added yet
                raise InternalServerError(
                    status_msg="Error occured while creating a new ticket"
                )
            else:
                logger.info("Ticket created successfully.")
                raise Success_200(status_msg="Ticket created successfully.")

    @token_required
    @users_required(users=["student", "support"])
    def put(self, ticket_id="", user_id=""):
        """
        Usage
        -----
        Update a ticket.
        # only student and support has access, role is checked later in code.
        Student who created a ticket can update : title, description, attachments, tags, priority
        Student who did not create : can vote a ticket
        Support can update : solution and attachment, status

        Parameters
        ----------
        form data sent with request

        Returns
        -------

        """
        details = {
            "title": "",
            "description": "",
            "tag_1": "",
            "tag_2": "",
            "tag_3": "",
            "priority": "",
            "status": "",
            "votes": 0,
            "solution": "",
        }

        # check url data
        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")

        # check form data
        try:
            form = request.get_json()
            attachments = form.get("attachments", [])
            for key in details:
                value = form.get(key, "")
                if ticket_utils.is_blank(value):
                    value = ""
                details[key] = value
        except Exception as e:
            logger.error(
                f"TicketAPI->put : Error occured while getting form data : {e}"
            )
            raise InternalServerError

        # check if ticket exists and it is created by user_id
        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
            ticket_attachment = TicketAttachment.query.filter_by(
                ticket_id=ticket_id
            ).all()
            user = Auth.query.filter_by(user_id=user_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->get : Error occured while fetching user and ticket data : {e}"
            )
            raise InternalServerError
        else:
            if not ticket:
                raise NotFoundError(status_msg="Ticket does not exists")
            if not user:
                raise NotFoundError(status_msg="User does not exists")

            role = user.role

            if role == "support" or (
                role == "student" and user_id == ticket.created_by
            ):
                # TODO : Handle attachment separatery, currently code is repeated
                for attach in attachments:  # received, dict
                    exists = False
                    for ticket_attach in ticket_attachment:  # already existing, object
                        if (
                            attach["user_id"] == ticket_attach.user_id
                            and attach["attachment_loc"] == ticket_attach.attachment_loc
                        ):
                            # can not add duplicate
                            exists = True
                            break
                    if not exists:
                        attach["ticket_id"] = ticket_id
                        ticket_attach = TicketAttachment(**attach)
                        db.session.add(ticket_attach)
                db.session.commit()

            if role == "student":
                if user_id == ticket.created_by:
                    # student is creator of the ticket
                    if details["title"] == "" or details["tag_1"] == "":
                        raise BadRequest(
                            status_msg=f"Ticket title and at least one tag is required"
                        )

                    ticket.title = details["title"]
                    ticket.description = details["description"]
                    ticket.tag_1 = details["tag_1"]
                    ticket.tag_2 = details["tag_2"]
                    ticket.tag_3 = details["tag_3"]
                    ticket.priority = details["priority"]

                    db.session.add(ticket)
                    db.session.commit()

                    raise Success_200(status_msg="Successfully updated a ticket.")

                else:
                    # student has not created this ticket, so only vote can be done
                    ticket_vote = TicketVote.query.filter_by(
                        ticket_id=ticket_id, user_id=user_id
                    ).first()
                    if ticket_vote:
                        # student has already voted
                        raise AlreadyExistError(
                            status_msg="You have already voted this ticket."
                        )
                    else:
                        # ticket upvoted
                        ticket_vote = TicketVote(ticket_id=ticket_id, user_id=user_id)
                        db.session.add(ticket_vote)

                        ticket.votes = ticket.votes + 1
                        db.session.add(ticket)

                        db.session.commit()
                        raise Success_200(status_msg="Successfully upvoted ticket.")

            if role == "support":
                sol = details["solution"]
                if ticket_utils.is_blank(sol):
                    raise BadRequest(status_msg="Solution can not be empty")
                else:
                    ticket.solution = sol
                    ticket.status = "resolved"

                    db.session.add(ticket)
                    db.session.commit()

                    raise Success_200(status_msg="Successfully resolved a ticket.")

            if role == "admin":
                # admin dont have access
                raise Unauthenticated(
                    status_msg="Admin don't have access to this endpoint."
                )

    @token_required
    @users_required(users=["student"])
    def delete(self, ticket_id="", user_id=""):
        """
        Usage
        -----
        Delete a single ticket. Only a student who created  a ticket can delete

        Parameters
        ----------
        ticket is and user id

        Returns
        -------


        """
        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")

        # check if ticket exists and it is created by user_id
        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->delete : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket:
                user = Auth.query.filter_by(user_id=user_id).first()
                if user_id == ticket.created_by:
                    # the ticket and its user are matched

                    # delete ticket votes
                    ticket_votes = TicketVote.query.filter_by(ticket_id=ticket_id).all()
                    for ticket_vote in ticket_votes:
                        db.session.delete(ticket_vote)
                    db.session.commit()

                    # delete ticket attachments
                    ticket_attachments = TicketAttachment.query.filter_by(
                        ticket_id=ticket_id
                    ).all()
                    for ticket_attachment in ticket_attachments:
                        db.session.delete(ticket_attachment)
                    db.session.commit()

                    # delete ticket
                    db.session.delete(ticket)
                    db.session.commit()
                    raise Success_200(status_msg="Ticket deleted successfully")
                else:
                    raise PermissionDenied(
                        status_msg="Only a user who created a ticket can delete it."
                    )
            else:
                raise NotFoundError(status_msg="Ticket does not exists")


class AllTicketsAPI(Resource):
    @token_required
    @users_required(users=['student', 'support', 'admin'])
    def get(self):
        """
        Usage
        -----
        Get all tickets.
        Url will contain a query and based on user role and query, tickets will 
        be retrieved -> filtered -> sorted -> then returned

        Student needs all tickets while searching and needs all their tickets (created and upvoted)
        Support needs pending tickets while resolving and needs all their resolved tickets
        Admin needs resolved tickets while creating FAQ
        
        - How it works:
        
        >>> params = {"query":"query", "filter":["tag_1", "tag_2"], "sortby":["a", "b"], "sortdir":["asc", "desc"], "status":"all", "priority":"all", 'user_specific':'No'}
        >>> resp = requests.get(url, params=params)
        >>> resp.url
        'https://BASE/api/v1/all-tickets?query=query&filter=tag_1&filter=tag_2&sortby=a&sortby=b&sortdir=asc&sortdir=desc&ticket_type=all....'

        Ticket status will be:
        - all : get all tickets from db (for student while searching)
        - pending: get all pending tickets from db (for support home page)
        - resolved: get all resolved tickets from db (for admin create faq page)

        Priority:
        all, low, medium, high

        If query is empty then get all tickets (created/upvoted by student or resolved by  support) where role will be checked from user_id
        

        Parameters
        ----------
        query

        Returns
        -------
        List of tickets 
        """
        # TODO : This API endpoint is working but not efficient. Can be updated later.

        def convert_arg_to_string(arg:str):
            # for internal use only, where arg is supposted to be a string 
            # but is converted to list due to 'flat=False'
            arg = args.get(arg, [])
            if arg == []:
                return ''
            else:
                return arg[0]


        # get query arguments
        try:
            args = request.args.to_dict(flat=False) # flat true returns only first items
            print(f'All Tickets : args : {args}')
            logger.debug(f'All Tickets : args : {args}')

            query = convert_arg_to_string("query")
            status = convert_arg_to_string("status")
            priority = convert_arg_to_string("priority")
            user_specific = convert_arg_to_string("user_specific")
            filter = args.get("filter", [])
            sortby = args.get("sortby", [])
            sortdir = args.get("sortdir", [])

            user_id = request.headers.get('user_id', '')
            
        except Exception as e:
            logger.error(
                f"AllTickets->get : Error occured while resolving query : {e}"
            )
            raise InternalServerError
        
        user = Auth.query.filter_by(user_id=user_id).first() # user already exists as user_required verified it
        
        # TODO: Search and Filter/Sort is not efficient. Update it if required
         
        if query:
            # user is student and is searching tickets while creating a new ticket.

            all_tickets = []

            # verify is user is student
            if user.role != "student":
                raise PermissionDenied(status_msg="Only student can search tickets using query.")

            # get all tickets
            tickets = Ticket.query.all()
            for ticket in tickets:
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)

            # match tickets with query
            all_tickets_1 = []
            for ticket in all_tickets:
                search_in = f"{ticket['title']} {ticket['description']} {ticket['solution']}"
                for q in query.split(' '):
                    if q.lower() in search_in.lower():
                        all_tickets_1.append(ticket)
                        break

            all_tickets = deepcopy(all_tickets_1)
                        
            # filter by tags only (if present)
            all_tickets_1 = []
            if filter:
                for ticket in all_tickets:
                    tags = [ticket['tag_1'], ticket['tag_2'], ticket['tag_3']] 
                    if set(tags).intersection(set(filter)):
                        all_tickets_1.append(ticket)

            all_tickets =  deepcopy(all_tickets_1)

            # sort (if present) 
            # TODO : Currently sorting is done by only one element. Multisort is disabled
            if (len(sortby)>=1) and (len(sortdir)>=1) and (len(sortby)==len(sortdir)):
                # sortby should be 'created_on', 'resolved_on', 'votes'
                if sortby not in ['created_on', 'resolved_on', 'votes']:
                    sortby = 'created_on'
                # sortdir should be 'asc' or 'desc'
                sortdir = True if sortdir=='desc' else False
                all_tickets = sorted(all_tickets, key=lambda d: d[sortby], reverse=sortdir)


            return success_200_custom(data=all_tickets)  

        else:
            # query is not present so for the user_id provided, get all tickets

            all_tickets = []

            # verify user role
            role = user.role
            
            if role == 'student':
                # student : all tickets created or upvoted by him/her
                # status, priority, sort, filter will be as per filter options received
                upvoted_ticket_ids = TicketVote.query.filter_by(user_id=user.user_id).all()
                upvoted_ticket_ids = [elem.ticket_id for elem in upvoted_ticket_ids]
                user_tickets = Ticket.query.filter_by(created_by=user.user_id).all()
                for ticket in user_tickets:
                    tick = ticket_utils.convert_ticket_to_dict(ticket)
                    all_tickets.append(tick)
                for ticket_id in upvoted_ticket_ids:
                    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
                    tick = ticket_utils.convert_ticket_to_dict(ticket)
                    all_tickets.append(tick)
                # upvoted ticket can be checked by comparing created_by with user_id

            if role == 'support':
                # support : all tickets resolvedby him/her where user_specific = Yes 
                # if user_specific = No, get all pending tickets 
                # status, priority, sort, filter will be as per filter options received
                # ? : user_specific is not used yet.

                if status == 'resolved' : # user_specific == 'Yes':
                    # get all tickets resolved by the support staff
                    user_tickets = Ticket.query.filter_by(resolved_by=user.user_id).all()
                    for ticket in user_tickets:
                        tick = ticket_utils.convert_ticket_to_dict(ticket)
                        all_tickets.append(tick)

                if status == 'pending' : # user_specific == 'No':
                    # get all pending tickets
                    user_tickets = Ticket.query.filter_by(status='pending').all()
                    for ticket in user_tickets:
                        tick = ticket_utils.convert_ticket_to_dict(ticket)
                        all_tickets.append(tick)

            if role == 'admin':
                # admin : all tickets resolved
                # status, priority, sort, filter will be as per filter options received

                # get all tickets resolved globally (for creating faq)
                user_tickets = Ticket.query.filter_by(status='resolved').all()
                for ticket in user_tickets:
                    tick = ticket_utils.convert_ticket_to_dict(ticket)
                    all_tickets.append(tick)

            
                        
            # check priority (if present)
            # priority : ['all', 'low', 'medium', 'high']
            all_tickets_1 = []
            if priority and priority in ['low', 'medium', 'high']:
                for ticket in all_tickets:
                    if ticket['priority'] == priority:
                        all_tickets_1.append(ticket)

            all_tickets =  deepcopy(all_tickets_1)

            # check status (if present)
            # status : ['all', 'pending', 'resolved']
            all_tickets_1 = []
            if status and status in ['pending', 'resolved'] and (role == 'student'):
                for ticket in all_tickets:
                    if ticket['status'] == status:
                        all_tickets_1.append(ticket)

            all_tickets =  deepcopy(all_tickets_1)

            # filter by tags only (if present)
            all_tickets_1 = []
            if filter:
                for ticket in all_tickets:
                    tags = [ticket['tag_1'], ticket['tag_2'], ticket['tag_3']] 
                    if set(tags).intersection(set(filter)):
                        all_tickets_1.append(ticket)

            all_tickets =  deepcopy(all_tickets_1)

            # sort (if present) 
            # TODO : Currently sorting is done by only one element. Multisort is disabled
            if (len(sortby)>=1) and (len(sortdir)>=1) and (len(sortby)==len(sortdir)):
                # sortby should be 'created_on', 'resolved_on', 'votes'
                if sortby not in ['created_on', 'resolved_on', 'votes']:
                    sortby = 'created_on'
                # sortdir should be 'asc' or 'desc'
                sortdir = True if sortdir=='desc' else False
                all_tickets = sorted(all_tickets, key=lambda d: d[sortby], reverse=sortdir)

            return success_200_custom(data=all_tickets) 
                

             


            
            
            
            

            


            
                        
            


             





        





        # if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
        #     raise BadRequest(status_msg="User id or ticket id is missing.")

        # # check if ticket exists and it is created by user_id
        # try:
        #     ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
        # except Exception as e:
        #     logger.error(
        #         f"TicketAPI->delete : Error occured while fetching ticket data : {e}"
        #     )
        #     raise InternalServerError
        # else:
        #     if ticket:
        #         user = Auth.query.filter_by(user_id=user_id).first()
        #         if user_id == ticket.created_by:
        #             # the ticket and its user are matched

        #             # delete ticket votes
        #             ticket_votes = TicketVote.query.filter_by(ticket_id=ticket_id).all()
        #             for ticket_vote in ticket_votes:
        #                 db.session.delete(ticket_vote)
        #             db.session.commit()

        #             # delete ticket attachments
        #             ticket_attachments = TicketAttachment.query.filter_by(
        #                 ticket_id=ticket_id
        #             ).all()
        #             for ticket_attachment in ticket_attachments:
        #                 db.session.delete(ticket_attachment)
        #             db.session.commit()

        #             # delete ticket
        #             db.session.delete(ticket)
        #             db.session.commit()
        #             raise Success_200(status_msg="Ticket deleted successfully")
        #         else:
        #             raise PermissionDenied(
        #                 status_msg="Only a user who created a ticket can delete it."
        #             )
        #     else:
        #         raise NotFoundError(status_msg="Ticket does not exists")


ticket_api.add_resource(
    TicketAPI,
    "/<string:ticket_id>/<string:user_id>",
    "/<string:user_id>",
)  # path is /api/v1/ticket
ticket_api.add_resource(AllTicketsAPI, "/all-tickets")

# --------------------  END  --------------------
