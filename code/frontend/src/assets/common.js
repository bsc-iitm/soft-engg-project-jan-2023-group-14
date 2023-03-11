/* eslint-disable */

const BASEURL = "http://127.0.0.1:5000";
const VERSION = "v1";
const AUTH_API_PREFIX = `/api/${VERSION}/auth`;
const STUDENT_API_PREFIX = `/api/${VERSION}/student`;
const AUTH_API_LOGIN = `${BASEURL}${AUTH_API_PREFIX}/login`
const AUTH_API_REGISTER = `${BASEURL}${AUTH_API_PREFIX}/register`


export { AUTH_API_LOGIN, AUTH_API_REGISTER, };
