

Testing CafeProtocolServer
==========================
 
Some test cases will focus on what the protocol server does when a request 
is received. In unit tests of this type, we want to create an instance of 
`CafeProtocolServer`, use it to "receive" one request (via the 
`receive_next_request` method), and validate that the expected method was 
called on the `CafeOrderHandler`

Other test cases will focus on whether responses are correctly represented.
In these unit tests, we'll invoke one of the `send_` methods and then inspect
what the protocol server "sent" to the client.

Server Protocol Testing Strategy
--------------------------------

* Create a mock implementation of `CafeIO` that allows us to pretend 
  a particular request was received and that allows us to inspect the
  response.
* Create a mock instance of `CafeOrderHandler` using Python's mock
  framework, which will allow us to determine whether the expected
  method call(s) occurred and to inspect method arguments as needed.
* Use Pytest _fixtures_ to inject these dependencies into each test case.
* Write separate small test case functions for everything we want to test.
* Run all our test cases with Pytest, and examine the output to find
  out what happened.

Test Case Outline for Handling Received Requests
------------------------------------------------

1. Define a function whose name starts with `test_` and with arguments
   that correspond to the names of the fixtures we need.
2. In the function, specify the string that corresponds to the client
   request we're pretending to have received. The request string is 
   specified as an attribute of the `MockCafeIO` fixture.
3. Call the protocol server's `receive_next_request` method.
4. Validate that the expected call was made on our mock `CafeProtocolServer`,
   (assuming that our test case is for a valid request). If testing an
   invalid request, validate that the `MockCafeIO` object collected any 
   expected error response strings.

Test Case Outline for Sending Responses
---------------------------------------

1. Define a function whose name starts with `test_` and with arguments
   that correspond to the names of the fixtures we need.
2. In the function, call one the `send_` methods on the protocol server.
3. Validate that the `MockCafeIO` object collected the expected response
   strings.


Testing CafeProtocolClient
==========================

In every unit test, we want to create an instance of `CafeProtocolClient`,
use it to "send" one request and get a (mock) response in return. We want
to be able to inspect the request sent by the client, and test how the
client handles normal responses and error responses.

Client Protocol Testing Strategy
--------------------------------

* Create a mock implementation of `CafeIO` that allows us to save and
  inspect the client's request, and to provide a mock response.
* Use Pytest _fixtures_ to inject these dependencies into each test case.
* Write separate small test case functions for everything we want to test.
* Run all our test cases with Pytest, and examine the output to find
  out what happened.

Test Case Outline
-----------------

1. Define a function whose name starts with `test_` and with arguments
   that correspond to the names of the fixtures we need.
2. In the function, specify the string that corresponds to the client
   request we're pretending to have received. The request string is 
   specified as an attribute of the `MockCafeIO` fixture.
3. Call the protocol server's `receive_next_request` method.
4. Validate that the expected call was made on our mock `CafeProtocolServer`,
   (assuming that our test case is for a valid request).
5. Validate that the `MockCafeIO` object collected the expected response
   strings.

   