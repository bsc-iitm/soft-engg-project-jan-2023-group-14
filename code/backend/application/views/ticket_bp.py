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
    convert_base64_to_img,
    convert_img_to_base64,
    is_img_path_valid,
    is_base64,
    get_encoded_file_details,
)
from application.views.user_utils import UserUtils
from application.responses import *
from application.models import *
from copy import deepcopy
from flask_cors import cross_origin
from application.globals import *
import base64

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
        # print(f"\n\n{ticket_dict}\n\n")
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

    def save_ticket_attachments(
        self, attachments: list, ticket_id: str, user_id: str, operation: str
    ):
        # get list of files from db for the ticket and user
        # if file already exists then add number extension
        # file name is not saved , only number extension required
        # currently there is no option to delete attachment
        # file name: {ticket_id}_{user_id}_{number-extension-if-needed}_.{file_format}
        # operation : create_ticket , update_ticket only student can do | resolve_ticket only support can do.

        total_attachments = len(attachments)
        num_successful_attachments = 0

        if total_attachments == 0:
            return (False, "Attachments are empty.")

        files = [
            file
            for file in os.listdir(TICKET_ATTACHMENTS_PATH)
            if file.startswith(f"{ticket_id}_{user_id}")
        ]
        number_extension = len(files)  # starting point

        for attach in attachments:
            # attach will be of format {attachment_loc:'', user_id:''}
            # attachment_loc will contain base64 version of image while data transfer is occuring between backend and frontend
            # attachment_loc will contain image path when data is retried from db by backend
            # attachment_loc will contain base64 image when creating new attachment

            if (user_id == attach["user_id"]) and (
                attach["attachment_loc"]
            ):  # redundant check
                if is_base64(attach["attachment_loc"].split(",")[1]):
                    file_type, file_format, encoded_data = get_encoded_file_details(
                        attach["attachment_loc"]
                    )
                    if (file_type == "image") and (
                        file_format in ACCEPTED_IMAGE_EXTENSIONS
                    ):
                        file_name = (
                            f"{ticket_id}_{user_id}_{number_extension}.{file_format}"
                        )
                        file_path = os.path.join(TICKET_ATTACHMENTS_PATH, file_name)
                        if convert_base64_to_img(file_path, encoded_data):
                            # successfully image saved and now add entry to database
                            try:
                                # while creating a ticket a student can upload multiple attachments
                                # verify whether each attachment is unique
                                attach["ticket_id"] = ticket_id
                                attach["attachment_loc"] = file_path
                                ticket_attach = TicketAttachment(**attach)
                                db.session.add(ticket_attach)
                                db.session.commit()
                                num_successful_attachments += 1
                                number_extension += 1
                            except Exception as e:
                                logger.error(
                                    f"TicketAPI->post : Error occured while creating a Ticket Attachment : {e}"
                                )
        return (
            True,
            f"Total {num_successful_attachments} / {total_attachments} attchements are valid and added successfully.",
        )


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

                # add attachments now
                status, message = ticket_utils.save_ticket_attachments(
                    attachments, ticket_id, user_id, operation="create_ticket"
                )
                raise Success_200(status_msg=f"Ticket created successfully. {message}")

            # try:
            #     # TODO : How to save attachments is not implemented
            #     # while creating a ticket a student can upload multiple attachments
            #     # verify whether each attachment is unique
            #     _attach = []
            #     for attach in attachments:
            #         if attach["attachment_loc"] in _attach:
            #             continue
            #         else:
            #             _attach.append(attach["attachment_loc"])
            #             attach["ticket_id"] = ticket_id
            #             ticket_attach = TicketAttachment(**attach)
            #             db.session.add(ticket_attach)
            #     db.session.commit()
            # except Exception as e:
            #     logger.error(
            #         f"TicketAPI->post : Error occured while creating a Ticket Attachment : {e}"
            #     )
            #     # TODO: db rollback not added yet
            #     raise InternalServerError(
            #         status_msg="Error occured while creating a Ticket Attachment"
            #     )

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
    @users_required(users=["student", "support", "admin"])
    def get(self):
        """
        Usage
        -----
        Get all tickets based on query and user role.
        Sorting and filtering will be applied as per query.

        Student needs all tickets while searching and needs all their tickets (created and upvoted)
        Support needs pending tickets while resolving and needs all their resolved tickets
        Admin needs resolved tickets while creating FAQ

        query sample: query=rgg&filter_priority=medium%2Clow&filter_status=pending&sortby=resolved_on&sortdir=

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

        def convert_arg_to_list(arg: str):
            # for internal use only
            arg = args.get(arg, "")
            if arg == "":
                return []
            else:
                return arg.split(",")

        # get query arguments
        try:
            args = request.args.to_dict(flat=True)
            print(f"All Tickets : args : {args}")
            logger.debug(f"All Tickets : args : {args}")

            query = args.get("query", "")
            status = convert_arg_to_list("filter_status")
            priority = convert_arg_to_list("filter_priority")
            tags = convert_arg_to_list("filter_tags")
            sortby = args.get("sortby", "")
            sortdir = args.get("sortdir", "")

            user_id = request.headers.get("user_id", "")
            print(f'User id: {user_id}')

        except Exception as e:
            logger.error(f"AllTickets->get : Error occured while resolving query : {e}")
            raise InternalServerError

        user = Auth.query.filter_by(
            user_id=user_id
        ).first()  # user already exists as user_required verified it

        # TODO: Search and Filter/Sort is not efficient. Update it if required

        if query:
            # user is student and is searching tickets while creating a new ticket.

            all_tickets = []

            # verify is user is student
            if user.role != "student":
                raise PermissionDenied(
                    status_msg="Only student can search tickets using query."
                )

            # get all tickets
            tickets = Ticket.query.all()
            for ticket in tickets:
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)

            print(f'Student search query - All tickets found : {len(all_tickets)}')

            # match tickets with query
            all_tickets_1 = []
            for ticket in all_tickets:
                search_in = (
                    f"{ticket['title']} {ticket['description']} {ticket['solution']}"
                )
                for q in query.split(" "):
                    if q.lower() in search_in.lower():
                        all_tickets_1.append(ticket)
                        break

            all_tickets = deepcopy(all_tickets_1)

            print(f'Student search query - query tickets found : {len(all_tickets)}')

            # filter by tags (if present)
            all_tickets_1 = []
            if tags:
                for ticket in all_tickets:
                    ticket_tags = [ticket["tag_1"], ticket["tag_2"], ticket["tag_3"]]
                    if set(ticket_tags).intersection(set(tags)):
                        all_tickets_1.append(ticket)

                all_tickets = deepcopy(all_tickets_1)

            print(f'Student search query - tags tickets found : {len(all_tickets)}')

            # filter by status (if present)
            all_tickets_1 = []
            if status:
                for ticket in all_tickets:
                    if ticket["status"] in status:
                        all_tickets_1.append(ticket)

                all_tickets = deepcopy(all_tickets_1)

            print(f'Student search query - status tickets found : {len(all_tickets)}')

            # filter by priority (if present)
            all_tickets_1 = []
            if priority:
                for ticket in all_tickets:
                    if ticket["priority"] in priority:
                        all_tickets_1.append(ticket)

                all_tickets = deepcopy(all_tickets_1)

            print(f'Student search query - priority tickets found : {len(all_tickets)}')

            # sort (if present)
            if sortby:
                # sortby should be 'created_on', 'resolved_on', 'votes'
                if sortby not in ["created_on", "resolved_on", "votes"]:
                    sortby = "created_on"
                # sortdir should be 'asc' or 'desc'
                sortdir = True if sortdir == "desc" else False

                is_sorting_valid = False
                for ticket in all_tickets:
                    if ticket["status"] == sortby: 
                        is_sorting_valid = True
                        break
                
                if is_sorting_valid:
                    all_tickets = sorted(
                        all_tickets, key=lambda d: d[sortby], reverse=sortdir
                    )

            print(f'Student search query - final sortby tickets found : {len(all_tickets)}')

            return success_200_custom(data=all_tickets)

        else:
            # query is not present so for the user_id provided, get all tickets

            all_tickets = []

            # verify user role
            role = user.role

            if role == "student":
                # student : all tickets created or upvoted by him/her
                # status, priority, sort, filter will be as per filter options received
                upvoted_ticket_ids = TicketVote.query.filter_by(
                    user_id=user.user_id
                ).all()
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

            if role == "support":
                # support : all tickets resolvedby him/her
                # get all pending tickets
                # status, priority, sort, filter will be as per filter options received

                if "resolved" in status:
                    # get all tickets resolved by the support staff
                    user_tickets = Ticket.query.filter_by(
                        resolved_by=user.user_id
                    ).all()
                    for ticket in user_tickets:
                        tick = ticket_utils.convert_ticket_to_dict(ticket)
                        all_tickets.append(tick)

                if "pending" in status:
                    # get all pending tickets
                    user_tickets = Ticket.query.filter_by(status="pending").all()
                    for ticket in user_tickets:
                        tick = ticket_utils.convert_ticket_to_dict(ticket)
                        all_tickets.append(tick)

            if role == "admin":
                # admin : all tickets resolved
                # status, priority, sort, filter will be as per filter options received

                # get all tickets resolved globally (for creating faq)
                user_tickets = Ticket.query.filter_by(status="resolved").all()
                for ticket in user_tickets:
                    tick = ticket_utils.convert_ticket_to_dict(ticket)
                    all_tickets.append(tick)

            
            # filter by tags (if present)
            all_tickets_1 = []
            if tags:
                for ticket in all_tickets:
                    ticket_tags = [ticket["tag_1"], ticket["tag_2"], ticket["tag_3"]]
                    if set(ticket_tags).intersection(set(tags)):
                        all_tickets_1.append(ticket)

                all_tickets = deepcopy(all_tickets_1)

            print(f'All tickets - tags tickets found : {len(all_tickets)}')

            # filter by status (if present)
            all_tickets_1 = []
            if status:
                for ticket in all_tickets:
                    if ticket["status"] in status:
                        all_tickets_1.append(ticket)

                all_tickets = deepcopy(all_tickets_1)

            print(f'All tickets  - status tickets found : {len(all_tickets)}')

            # filter by priority (if present)
            all_tickets_1 = []
            if priority:
                for ticket in all_tickets:
                    if ticket["priority"] in priority:
                        all_tickets_1.append(ticket)

                all_tickets = deepcopy(all_tickets_1)

            print(f'All tickets  - priority tickets found : {len(all_tickets)}')

            
            # sort (if present)
            if sortby:
                # sortby should be 'created_on', 'resolved_on', 'votes'
                if sortby not in ["created_on", "resolved_on", "votes"]:
                    sortby = "created_on"
                # sortdir should be 'asc' or 'desc'
                sortdir = True if sortdir == "desc" else False
                
                is_sorting_valid = False
                for ticket in all_tickets:
                    if ticket["status"] == sortby: 
                        is_sorting_valid = True
                        break
                
                if is_sorting_valid:
                    all_tickets = sorted(
                        all_tickets, key=lambda d: d[sortby], reverse=sortdir
                    )

            print(f'All tickets - final sortby tickets found : {len(all_tickets)}')

            return success_200_custom(data=all_tickets)


ticket_api.add_resource(
    TicketAPI,
    "/<string:ticket_id>/<string:user_id>",
    "/<string:user_id>",
)  # path is /api/v1/ticket
ticket_api.add_resource(AllTicketsAPI, "/all-tickets")

# --------------------  END  --------------------

# class AllTicketsAPI(Resource):
#     @token_required
#     @users_required(users=["student", "support", "admin"])
#     def get(self):
#         """
#         Usage
#         -----
#         Get all tickets.
#         Url will contain a query and based on user role and query, tickets will
#         be retrieved -> filtered -> sorted -> then returned

#         Student needs all tickets while searching and needs all their tickets (created and upvoted)
#         Support needs pending tickets while resolving and needs all their resolved tickets
#         Admin needs resolved tickets while creating FAQ

#         - How it works:

#         >>> params = {"query":"query", "filter":["tag_1", "tag_2"], "sortby":["a", "b"], "sortdir":["asc", "desc"], "status":"all", "priority":"all"}
#         >>> resp = requests.get(url, params=params)
#         >>> resp.url
#         'https://BASE/api/v1/all-tickets?query=query&filter=tag_1&filter=tag_2&sortby=a&sortby=b&sortdir=asc&sortdir=desc&ticket_type=all....'

#         Ticket status will be:
#         - all : get all tickets from db (for student while searching)
#         - pending: get all pending tickets from db (for support home page)
#         - resolved: get all resolved tickets from db (for admin create faq page)

#         Priority:
#         all, low, medium, high

#         If query is empty then get all tickets (created/upvoted by student or resolved by  support) where role will be checked from user_id


#         Parameters
#         ----------
#         query

#         Returns
#         -------
#         List of tickets
#         """
#         # TODO : This API endpoint is working but not efficient. Can be updated later.

#         def convert_arg_to_string(arg: str):
#             # for internal use only, where arg is supposted to be a string
#             # but is converted to list due to 'flat=False'
#             arg = args.get(arg, [])
#             if arg == []:
#                 return ""
#             else:
#                 return arg[0]

#         # get query arguments
#         try:
#             args = request.args.to_dict(
#                 flat=False
#             )  # flat true returns only first items
#             print(f"All Tickets : args : {args}")
#             logger.debug(f"All Tickets : args : {args}")

#             query = convert_arg_to_string("query")
#             status = convert_arg_to_string("status")
#             priority = convert_arg_to_string("priority")
#             filter = args.get("filter", [])
#             sortby = args.get("sortby", [])
#             sortdir = args.get("sortdir", [])

#             user_id = request.headers.get("user_id", "")

#         except Exception as e:
#             logger.error(f"AllTickets->get : Error occured while resolving query : {e}")
#             raise InternalServerError

#         user = Auth.query.filter_by(
#             user_id=user_id
#         ).first()  # user already exists as user_required verified it

#         # TODO: Search and Filter/Sort is not efficient. Update it if required

#         if query:
#             # user is student and is searching tickets while creating a new ticket.

#             all_tickets = []

#             # verify is user is student
#             if user.role != "student":
#                 raise PermissionDenied(
#                     status_msg="Only student can search tickets using query."
#                 )

#             # get all tickets
#             tickets = Ticket.query.all()
#             for ticket in tickets:
#                 tick = ticket_utils.convert_ticket_to_dict(ticket)
#                 all_tickets.append(tick)

#             # match tickets with query
#             all_tickets_1 = []
#             for ticket in all_tickets:
#                 search_in = (
#                     f"{ticket['title']} {ticket['description']} {ticket['solution']}"
#                 )
#                 for q in query.split(" "):
#                     if q.lower() in search_in.lower():
#                         all_tickets_1.append(ticket)
#                         break

#             all_tickets = deepcopy(all_tickets_1)

#             # filter by tags only (if present)
#             all_tickets_1 = []
#             if filter:
#                 for ticket in all_tickets:
#                     tags = [ticket["tag_1"], ticket["tag_2"], ticket["tag_3"]]
#                     if set(tags).intersection(set(filter)):
#                         all_tickets_1.append(ticket)

#             all_tickets = deepcopy(all_tickets_1)

#             # sort (if present)
#             # TODO : Currently sorting is done by only one element. Multisort is disabled
#             if (
#                 (len(sortby) >= 1)
#                 and (len(sortdir) >= 1)
#                 and (len(sortby) == len(sortdir))
#             ):
#                 # sortby should be 'created_on', 'resolved_on', 'votes'
#                 if sortby not in ["created_on", "resolved_on", "votes"]:
#                     sortby = "created_on"
#                 # sortdir should be 'asc' or 'desc'
#                 sortdir = True if sortdir == "desc" else False
#                 all_tickets = sorted(
#                     all_tickets, key=lambda d: d[sortby], reverse=sortdir
#                 )

#             return success_200_custom(data=all_tickets)

#         else:
#             # query is not present so for the user_id provided, get all tickets

#             all_tickets = []

#             # verify user role
#             role = user.role

#             if role == "student":
#                 # student : all tickets created or upvoted by him/her
#                 # status, priority, sort, filter will be as per filter options received
#                 upvoted_ticket_ids = TicketVote.query.filter_by(
#                     user_id=user.user_id
#                 ).all()
#                 upvoted_ticket_ids = [elem.ticket_id for elem in upvoted_ticket_ids]
#                 user_tickets = Ticket.query.filter_by(created_by=user.user_id).all()
#                 for ticket in user_tickets:
#                     tick = ticket_utils.convert_ticket_to_dict(ticket)
#                     all_tickets.append(tick)
#                 for ticket_id in upvoted_ticket_ids:
#                     ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
#                     tick = ticket_utils.convert_ticket_to_dict(ticket)
#                     all_tickets.append(tick)
#                 # upvoted ticket can be checked by comparing created_by with user_id

#             if role == "support":
#                 # support : all tickets resolvedby him/her
#                 # get all pending tickets
#                 # status, priority, sort, filter will be as per filter options received

#                 if status == "resolved":
#                     # get all tickets resolved by the support staff
#                     user_tickets = Ticket.query.filter_by(
#                         resolved_by=user.user_id
#                     ).all()
#                     for ticket in user_tickets:
#                         tick = ticket_utils.convert_ticket_to_dict(ticket)
#                         all_tickets.append(tick)

#                 if status == "pending":
#                     # get all pending tickets
#                     user_tickets = Ticket.query.filter_by(status="pending").all()
#                     for ticket in user_tickets:
#                         tick = ticket_utils.convert_ticket_to_dict(ticket)
#                         all_tickets.append(tick)

#             if role == "admin":
#                 # admin : all tickets resolved
#                 # status, priority, sort, filter will be as per filter options received

#                 # get all tickets resolved globally (for creating faq)
#                 user_tickets = Ticket.query.filter_by(status="resolved").all()
#                 for ticket in user_tickets:
#                     tick = ticket_utils.convert_ticket_to_dict(ticket)
#                     all_tickets.append(tick)

#             # check priority (if present)
#             # priority : ['all', 'low', 'medium', 'high']
#             all_tickets_1 = []
#             if priority and priority in ["low", "medium", "high"]:
#                 for ticket in all_tickets:
#                     if ticket["priority"] == priority:
#                         all_tickets_1.append(ticket)

#             all_tickets = deepcopy(all_tickets_1)

#             # check status (if present)
#             # status : ['all', 'pending', 'resolved']
#             all_tickets_1 = []
#             if status and status in ["pending", "resolved"] and (role == "student"):
#                 for ticket in all_tickets:
#                     if ticket["status"] == status:
#                         all_tickets_1.append(ticket)

#             all_tickets = deepcopy(all_tickets_1)

#             # filter by tags only (if present)
#             all_tickets_1 = []
#             if filter:
#                 for ticket in all_tickets:
#                     tags = [ticket["tag_1"], ticket["tag_2"], ticket["tag_3"]]
#                     if set(tags).intersection(set(filter)):
#                         all_tickets_1.append(ticket)

#             all_tickets = deepcopy(all_tickets_1)

#             # sort (if present)
#             # TODO : Currently sorting is done by only one element. Multisort is disabled
#             if (
#                 (len(sortby) >= 1)
#                 and (len(sortdir) >= 1)
#                 and (len(sortby) == len(sortdir))
#             ):
#                 # sortby should be 'created_on', 'resolved_on', 'votes'
#                 if sortby not in ["created_on", "resolved_on", "votes"]:
#                     sortby = "created_on"
#                 # sortdir should be 'asc' or 'desc'
#                 sortdir = True if sortdir == "desc" else False
#                 all_tickets = sorted(
#                     all_tickets, key=lambda d: d[sortby], reverse=sortdir
#                 )

#             return success_200_custom(data=all_tickets)
