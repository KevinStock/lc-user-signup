#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

form = """
    <form method="post">
        <table>
            <tr>
                <td>
                    <label for="username">Username</label>
                </td>
                <td>
                    <input type="text" required name="username" value="%(username)s" />
                    <span style="color: red">%(username_error)s</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="password">Password</label>
                </td>
                <td>
                    <input type="password" required name="password" />
                    <span style="color: red">%(password_error)s</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="passwordConfirm">Confirm Password</label>
                </td>
                <td>
                    <input type="password" required name="passwordConfirm" />
                    <span style="color: red">%(passwordConfirm_error)s</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="email">Email (optional)</label>
                </td>
                <td>
                    <input type="email" name="email" value="%(email)s"/>
                    <span style="color: red">%(email_error)s</span>
                </td>
            </tr>
        </table>
        <input type="submit" value="Sign Up" />
    </form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASS_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):

    def write_form(self, username_error="", password_error="", passwordConfirm_error="", email_error="", username="", email=""):
        self.response.out.write(form % {"username_error": username_error,
                                        "password_error": password_error,
                                        "passwordConfirm_error": passwordConfirm_error,
                                        "email_error": email_error,
                                        "username": username,
                                        "email": email})

    def get(self):
        self.write_form()

    def post(self):
        error = ""
        username = self.request.get("username")
        password = self.request.get("password")
        passwordConfirm = self.request.get("passwordConfirm")
        email = self.request.get("email")
        username_error = ""
        password_error = ""
        passwordConfirm_error = ""
        email_error = ""
        error = False
        
        if not username:
            username_error = "Username cannot be left blank"
            error = True
        if valid_username(username) == None:
            username_error = "Username is invalid"
            error = True

        if not password:
            if not passwordConfirm:
                passwordConfirm_error = "Password cannot be left blank"
            password_error = "Password cannot be left blank"
            error = True
        elif valid_password(password) == None:
            password_error = "Password is invalid"
            error = True

        if password != passwordConfirm:
            passwordConfirm_error = "Passwords do not match"
            error = True

        if email and valid_email(email) == None:
            email_error = "Email is invalid"
            error = True

        if error:
            self.write_form(username_error, password_error, passwordConfirm_error, email_error, username, email)
        else:
            self.redirect("/welcome?name=" + username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("name")
        self.response.out.write("<h1>Welcome, " + username + "!</h1>")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
