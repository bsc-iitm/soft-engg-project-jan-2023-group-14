/* eslint-disable */

const BASEURL = "http://127.0.0.1:5000";
const VERSION = "v1";

const AUTH_API_PREFIX = `/api/${VERSION}/auth`;
const STUDENT_API_PREFIX = `/api/${VERSION}/student`;
const SUPPORT_API_PREFIX = `/api/${VERSION}/support`;
const ADMIN_API_PREFIX = `/api/${VERSION}/admin`;
const FAQ_API_PREFIX = `/api/${VERSION}/faq`;
const TICKET_API_PREFIX = `/api/${VERSION}/ticket`

const AUTH_API_LOGIN = `${BASEURL}${AUTH_API_PREFIX}/login`
const AUTH_API_REGISTER = `${BASEURL}${AUTH_API_PREFIX}/register`
const AUTH_API_NEWUSERS = `${BASEURL}${AUTH_API_PREFIX}/newUsers`

const STUDENT_API = `${BASEURL}${STUDENT_API_PREFIX}`;
const SUPPORT_API = `${BASEURL}${SUPPORT_API_PREFIX}`;
const ADMIN_API = `${BASEURL}${ADMIN_API_PREFIX}`;
const FAQ_API = `${BASEURL}${FAQ_API_PREFIX}`;
const TICKET_API = `${BASEURL}${TICKET_API_PREFIX}`;

const TICKET_API_ALLTICKETS = `${BASEURL}${TICKET_API_PREFIX}/all-tickets`


const STUDENT_ROUTES = ['/student', '/student-home', "/student-create-ticket", "/student-my-tickets", "/common-faqs"]
const SUPPORT_ROUTES = ['/support', '/support-home']
const ADMIN_ROUTES = ['/admin', '/admin-home']


export {
  AUTH_API_LOGIN,
  AUTH_API_REGISTER, 
  AUTH_API_NEWUSERS,
  STUDENT_API_PREFIX,
  SUPPORT_API_PREFIX,
  ADMIN_API_PREFIX,
  FAQ_API_PREFIX,
  TICKET_API_ALLTICKETS,
  TICKET_API_PREFIX,
  STUDENT_API,
  SUPPORT_API,
  ADMIN_API,
  FAQ_API,
  TICKET_API,
  STUDENT_ROUTES, 
  SUPPORT_ROUTES, 
  ADMIN_ROUTES,
};
