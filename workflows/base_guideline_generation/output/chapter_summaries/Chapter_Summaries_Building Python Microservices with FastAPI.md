# Comprehensive Python Guidelines — Building Python Microservices with FastAPI (Chapters 1-14)

*Source: Building Python Microservices with FastAPI, Chapters 1-14*

---

## Chapter 1: Setting Up FastAPI for Starters

*Source: Building Python Microservices with FastAPI, pages 1–26*

### Chapter Summary
Introduces FastAPI framework fundamentals including installation, setup, and basic configuration. Covers Uvicorn ASGI server, Pydantic integration, Starlette foundation, and creating first REST API endpoints with async support. [^1]

### Concept-by-Concept Breakdown
#### **None** *(p.21)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.21, lines 17–24)*:
```
def login(username: str, password: str):
    if valid_users.get(username) == None:
        return {"message": "user does not exist"}
    else:
        user = valid_users.get(username)
Any command-line input or output is written as follows:
pip install fastapi
pip install uvicorn[standard]
```
[^2]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.15)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.15, lines 7–14)*:
```
333
Creating arrays and 
DataFrames
334
Applying NumPy’s linear system 
operations
335
Applying the pandas module
```
[^3]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.19)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.19, lines 2–9)*:
```
xviii
Chapter 6, Using a Non-Relational Database, showcases the PyMongo and Motor engines, including 
some popular Python Object Document Mapper (ODMs), which can connect FastAPI applications 
to a MongoDB server.
Chapter 7, Securing the REST APIs, highlights FastAPI’s built-in security module classes and explores 
some third-party tools such as JWT, Keycloak, Okta, and Auth0 and how they are applied to implement 
different security schemes to secure an application.
Chapter 8, Creating Coroutines, Events, and Message-Driven Transactions, focuses on the details of 
```
[^4]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 25 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.13)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.13, lines 25–32)*:
```
254
Designing asynchronous 
transactions
258
Using the HTTP/2 protocol
261
Creating asynchronous 
background tasks
```
[^5]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.10)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.10, lines 84–91)*:
```
124
Installing the asyncio-compliant 
database drivers
124
Setting up the database’s 
connection
124
Creating the session factory
```
[^6]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.10)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.10, lines 44–51)*:
```
Storing settings as class 
attributes
101
Storing settings in the properties 
file
102
Summary
104
```
[^7]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.10)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.10, lines 43–50)*:
```
100
Storing settings as class 
attributes
101
Storing settings in the properties 
file
102
Summary
```
[^8]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Coroutine** *(p.13)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.13, lines 17–24)*:
```
8
Creating Coroutines, Events, and Message-Driven Transactions	
253
Technical requirements
254
Implementing coroutines
254
Applying coroutine switching
```
[^9]
**Annotation:** This excerpt demonstrates 'coroutine' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.15)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.15, lines 18–25)*:
```
337
Generating CSV and XLSX 
reports
338
Plotting data models
342
Simulating a BPMN 
workflow
```
[^10]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Custom Exception** *(p.9)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.9, lines 8–15)*:
```
33
Custom exceptions
34
A default handler override
37
Converting objects to JSON-
compatible types
38
```
[^11]
**Annotation:** This excerpt demonstrates 'custom exception' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Dataframe** *(p.15)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.15, lines 8–15)*:
```
Creating arrays and 
DataFrames
334
Applying NumPy’s linear system 
operations
335
Applying the pandas module
336
```
[^12]
**Annotation:** This excerpt demonstrates 'dataframe' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Decorator** *(p.18)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.18, lines 15–22)*:
```
Chapter 1, Setting Up FastAPI for Starters, introduces how to create FastAPI endpoints using the 
core module classes and decorators and how the framework manages incoming API requests and 
outgoing responses.
Chapter 2, Exploring the Core Features, introduces FastAPI’s asynchronous endpoints, exception 
handling mechanism, background processes, APIRouter for project organization, the built-in JSON 
encoder, and FastAPI’s JSON responses.
Chapter 3, Investigating Dependency Injection, explores the Dependency Injection (DI) pattern 
utilized by FastAPI to manage instances and project structure using its Depends() directive and 
```
[^13]
**Annotation:** This excerpt demonstrates 'decorator' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.11)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.11, lines 30–37)*:
```
141
Defining the model classes
141
Implementing the CRUD 
transactions
144
Running the repository 
transactions
```
[^14]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Dictionary** *(p.12)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.12, lines 80–87)*:
```
231
Building the permission dictionary
232
Implementing the login transaction
233
Applying the scopes to endpoints
234
Building the authorization 
```
[^15]
**Annotation:** This excerpt demonstrates 'dictionary' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.21)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.21, lines 19–26)*:
```
        return {"message": "user does not exist"}
    else:
        user = valid_users.get(username)
Any command-line input or output is written as follows:
pip install fastapi
pip install uvicorn[standard]
Bold: Indicates a new term, an important word, or words that you see onscreen. For instance, 
words in menus or dialog boxes appear in bold. Here is an example: "Select System info from the 
```
[^16]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 2: Exploring the Core Features** *(pp.27–60)*

This later chapter builds upon the concepts introduced here, particularly: None, as, async.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^17]

**Annotation:** Forward reference: Chapter 2 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 3: Investigating Dependency Injection** *(pp.61–88)*

This later chapter builds upon the concepts introduced here, particularly: None, as, async.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^18]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Building the Microservice Application** *(pp.89–130)*

This later chapter builds upon the concepts introduced here, particularly: None, as, async.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^19]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 2: Exploring the Core Features

*Source: Building Python Microservices with FastAPI, pages 27–60*

### Chapter Summary
Explores FastAPI's core features including path operations, routing, request/response handling, Pydantic validation and schemas, HTTP methods, query and path parameters, request bodies, and status code management. [^20]

### Concept-by-Concept Breakdown
#### **None** *(p.38)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.38, lines 16–23)*:
```
supposed data type of the parameter using brackets ([]) and can have any default value if needed. 
Assigning the Optional parameter to a None value indicates that its exclusion from the parameter 
passing is allowed by the service, but it will hold a None value. The following services depict the use 
of optional parameters:
from typing import Optional, List, Dict
@app.post("/ch01/login/username/unlock")
def unlock_username(id: Optional[UUID] = None):
    if id == None:
```
[^21]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.57)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.57, lines 17–24)*:
```
class PostFeedbackException(HTTPException):
    def __init__(self, detail: str, status_code: int):
        self.status_code = status_code
        self.detail = detail
        
class PostRatingException(HTTPException):
    def __init__(self, detail: str, status_code: int):
        self.status_code = status_code
```
[^22]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Annotation** *(p.33)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.33, lines 15–22)*:
```
The framework also supports the data types included in Python’s typing module, responsible for 
type hints. These data types are standard notations for Python and variable type annotations that can 
help to pursue type checking and model validation during compilation, such as Optional, List, 
Dict, Set, Union, Tuple, FrozenSet, Iterable, and Deque.
Path parameters
FastAPI allows you to obtain request data from the endpoint URL of an API through a path parameter 
or path variable that makes the URL somewhat dynamic. This parameter holds a value that becomes 
part of a URL indicated by curly braces ({}). After setting off these path parameters within the URL, 
```
[^23]
**Annotation:** This excerpt demonstrates 'annotation' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.38)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.38, lines 5–12)*:
```
            return {"message": "invalid user"}
delete_pending_users() can be executed even without passing any accounts argument, 
since accounts will be always an empty List by default. Likewise, change_password() can 
still continue its process without passing any old_passwd and new_passw, since they are both 
always defaulted to empty str. hashpw() is a bcrypt utility function that generates a hashed 
passphrase from an autogenerated salt.
Optional parameters
If the path and/or query parameter(s) of a service is/are not necessarily needed to be supplied by 
```
[^24]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.37)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.37, lines 1–8)*:
```
Setting Up FastAPI for Starters
14
Default parameters
There are times that we need to specify default values to the query parameter(s) and path parameter(s) 
of some API services to avoid validation error messages such as field required and value_
error.missing. Setting default values to parameters will allow the execution of an API method 
with or without supplying the parameter values. Depending on the requirement, assigned default values 
are usually 0 for numeric types, False for bool types, empty string for string types, an empty list 
```
[^25]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 29 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.28)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.28, lines 5–12)*:
```
module is required to create a REST API that handles form parameters. The installed uvicorn, 
however, is an ASGI-based server that will run your FastAPI applications. The Asynchronous Server 
Gateway Interface (ASGI) server that FastAPI uses makes it the fastest Python framework at the time 
of writing. The uvicorn server has the capability to run both synchronous and asynchronous services.
After the installation and configuration of the essential tools, modules, and IDE, let us now start our 
first API implementation using the framework.
Initializing and configuring FastAPI
Learning how to create applications using FastAPI is easy and straightforward. A simple application can 
```
[^26]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.41)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.41, lines 2–9)*:
```
18
The attributes of the model classes must be explicitly declared by applying type hints and utilizing the 
common and complex data types used in the parameter declaration. These attributes can also be set 
as required, default, and optional, just like in the parameters.
Moreover, the pydantic module allows the creation of nested models, even the deeply nested ones. 
A sample of these is shown here:    
class ForumPost(BaseModel):
    id: UUID
```
[^27]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.40)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.40, lines 19–26)*:
```
represent and capture this request body to be processed for further results.
To implement a model class for the request body, you should first import the BaseModel class 
from the pydantic module. Then, create a subclass of it to utilize all the properties and behavior 
needed by the path operation in capturing the request body. Here are some of the data models used 
by our application:
from pydantic import BaseModel
class User(BaseModel):
    username: str
```
[^28]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.27)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.27, lines 7–14)*:
```
reading this chapter. It is not designed to use any database management system, but all the data is 
temporarily stored in various Python collections. All the applications in this book are compiled and 
run using Python 3.8. Codes are all uploaded at https://github.com/PacktPublishing/
Building-Python-Microservices-with-FastAPI/tree/main/ch01.
Setting up the development environment
The FastAPI framework is a fast, seamless, and robust Python framework but can only work on Python 
versions 3.6 and above. The Integrated Development Environment (IDE) used in this reference is 
Visual Studio Code (VS Code), which is an open source tool that we can download from this site: 
```
[^29]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Compiled** *(p.27)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.27, lines 7–14)*:
```
reading this chapter. It is not designed to use any database management system, but all the data is 
temporarily stored in various Python collections. All the applications in this book are compiled and 
run using Python 3.8. Codes are all uploaded at https://github.com/PacktPublishing/
Building-Python-Microservices-with-FastAPI/tree/main/ch01.
Setting up the development environment
The FastAPI framework is a fast, seamless, and robust Python framework but can only work on Python 
versions 3.6 and above. The Integrated Development Environment (IDE) used in this reference is 
Visual Studio Code (VS Code), which is an open source tool that we can download from this site: 
```
[^30]
**Annotation:** This excerpt demonstrates 'compiled' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Constructor** *(p.42)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.42, lines 27–34)*:
```
the request body to the BaseModel model. Second, to instantiate a BaseModel class, all its 
required attributes must be initialized immediately through the constructor’s named parameters.
Request headers
In a request-response transaction, it is not only the parameters that are accessible by the REST API 
methods but also the information that describes the context of the client where the request originated. 
Some common request headers such as User-Agent, Host, Accept, Accept-Language, 
Accept-Encoding, Referer, and Connection usually appear with request parameters and 
values during request transactions.
```
[^31]
**Annotation:** This excerpt demonstrates 'constructor' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.38)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.38, lines 7–14)*:
```
since accounts will be always an empty List by default. Likewise, change_password() can 
still continue its process without passing any old_passwd and new_passw, since they are both 
always defaulted to empty str. hashpw() is a bcrypt utility function that generates a hashed 
passphrase from an autogenerated salt.
Optional parameters
If the path and/or query parameter(s) of a service is/are not necessarily needed to be supplied by 
the user, meaning the API transactions can proceed with or without their inclusion in the request 
transaction, then we set them as optional. To declare an optional parameter, we need to import the 
```
[^32]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Custom Exception** *(p.57)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.57, lines 7–14)*:
```
HTTPException, halting all the operations in order to return an error message.
Custom exceptions
It is also possible to create a user-defined HTTPException object to handle business-specific 
problems. This custom exception requires a custom handler needed to manage its response to the client 
whenever an operation raises it. These custom components should be available to all API methods 
across the project structure; thus, they must be implemented at the project-folder level.
In our application, there are two custom exceptions created in handler_exceptions.py, the 
PostFeedbackException and PostRatingFeedback exceptions, which handle problems 
```
[^33]
**Annotation:** This excerpt demonstrates 'custom exception' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Datetime** *(p.33)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.33, lines 12–19)*:
```
bool, int, and float and container types such as list, tuple, dict, set, frozenset, and 
deque. Other complex Python types such as datetime.date, datetime.time, datetime.
datetime, datetime.delta, UUID, bytes, and Decimal are also supported. 
The framework also supports the data types included in Python’s typing module, responsible for 
type hints. These data types are standard notations for Python and variable type annotations that can 
help to pursue type checking and model validation during compilation, such as Optional, List, 
Dict, Set, Union, Tuple, FrozenSet, Iterable, and Deque.
Path parameters
```
[^34]
**Annotation:** This excerpt demonstrates 'datetime' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Decorator** *(p.28)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.28, lines 18–25)*:
```
from the fastapi module and use app as the reference variable to the object. Then, this object is 
used later as a Python @app decorator, which provides our application with some features such as 
routes, middleware, exception handlers, and path operations.
Important note
You can replace app with your preferred but valid Python variable name, such as main_app, 
forum, or myapp.
Now, your application is ready to manage REST APIs that are technically Python functions. But to 
declare them as REST service methods, we need to decorate them with the appropriate HTTP request 
```
[^35]
**Annotation:** This excerpt demonstrates 'decorator' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 3: Investigating Dependency Injection** *(pp.61–88)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^36]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Building the Microservice Application** *(pp.89–130)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^37]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Connecting to a Relational Database** *(pp.131–162)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^38]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 3: Investigating Dependency Injection

*Source: Building Python Microservices with FastAPI, pages 61–88*

### Chapter Summary
Details dependency injection system in FastAPI using Depends. Covers creating reusable dependencies, managing database sessions, implementing security dependencies, middleware patterns, and understanding dependency scopes and context management. [^39]

### Concept-by-Concept Breakdown
#### **None** *(p.63)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.63, lines 33–36)*:
```
def show_booked_tours(touristId: UUID):
    if approved_users.get(touristId) == None:
         raise HTTPException(
         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
```
[^40]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.75)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.75, lines 11–18)*:
```
class Login:
    def __init__(self, id: UUID, username: str, 
                 password: str, type: UserType): 
        self.id = id
        self.username = username
        self.password = password
        self.type= type
class UserDetails: 
```
[^41]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.68)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.68, lines 22–29)*:
```
first one is Request and the second one is a function called call_next(), which takes the 
Request parameter as its argument to return the response. Then, decorate the method with @app.
middleware("http") to inject the component into the framework.
The tourist application has one middleware implemented by the asynchronous add_transaction_
filter() here that logs the necessary request data of a particular API method before its execution 
and modifies its response object by adding a response header, X-Time-Elapsed, which carries 
the running time of the execution. 
The execution of await call_next(request) is the most crucial part of the middleware 
```
[^42]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.66)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.66, lines 1–8)*:
```
Using asynchronous path operations
43
Using asynchronous path operations
When it comes to improving performance, FastAPI is an asynchronous framework, and it uses Python’s 
AsyncIO principles and concepts to create a REST API implementation that can run separately and 
independently from the application’s main thread. The idea also applies to how a background task is 
executed. Now, to create an asynchronous REST endpoint, attach async to the func signature of 
the service:
```
[^43]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 22 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.66)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.66, lines 1–8)*:
```
Using asynchronous path operations
43
Using asynchronous path operations
When it comes to improving performance, FastAPI is an asynchronous framework, and it uses Python’s 
AsyncIO principles and concepts to create a REST API implementation that can run separately and 
independently from the application’s main thread. The idea also applies to how a background task is 
executed. Now, to create an asynchronous REST endpoint, attach async to the func signature of 
the service:
```
[^44]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 13 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.66)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.66, lines 4–11)*:
```
When it comes to improving performance, FastAPI is an asynchronous framework, and it uses Python’s 
AsyncIO principles and concepts to create a REST API implementation that can run separately and 
independently from the application’s main thread. The idea also applies to how a background task is 
executed. Now, to create an asynchronous REST endpoint, attach async to the func signature of 
the service:
@router.get("/feedback/list")
async def show_tourist_post(touristId: UUID):
    tourist_posts = [assess for assess in feedback_tour.
```
[^45]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.62)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.62, lines 7–14)*:
```
created user to be approved by the administrator. If you observe the Tourist model class, it has a 
date_signed attribute that is declared as datettime, and temporal types are not always JSON-
friendly. Having model objects with non-JSON-friendly components in FastAPI-related operations 
can cause serious exceptions. To avoid these Pydantic validation issues, it is always advisable to use 
jsonable_encoder() to manage the conversion of all the attributes of our model object into 
JSON-types.
Important note
The json module with its dumps() and loads() utility methods can be used instead of 
```
[^46]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.67)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.67, lines 6–13)*:
```
    for key in post_delete:
        is_owner = await check_post_owner(feedback_tour, 
                       access.id, touristId)
        if is_owner:
            del feedback_tour[access.id]
    return JSONResponse(content={"message" : f"deleted
          posts of {touristId}"}, status_code=200)
delete_tourist_feedback() here is an asynchronous REST API endpoint that calls an 
```
[^47]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.88)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.88, lines 8–15)*:
```
              ingrA5, ingrA6, ingrA7, ingrA8, ingrA9], 
         cat= Category.breakfast, 
         name='Crustless quiche bites with asparagus and 
               oven-dried tomatoes', 
         id=uuid1())
        ingrB1 = Ingredient(measure='tablespoon', qty=1, 
           name='oil', id=uuid1())
        ingrB2 = Ingredient(measure='cup', qty=0.5, 
```
[^48]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.73)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.73, lines 5–12)*:
```
providers, or components.
Injecting a callable class
FastAPI also allows classes to be injected into any components, since they can also be considered 
callable components. A class becomes callable during instantiation when the call to its constructor, 
__init__(self), is done. Some of these classes have no-arg constructors, while others, such as 
the following Login class, require constructor arguments:
class Login:
    def __init__(self, id: UUID, username: str, 
```
[^49]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.81)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.81, lines 10–17)*:
```
    return post
The validator will always work closely with the incoming request transaction, whereas the other two 
injectables, post and handler, are part of the API’s transactions.
Important Note
The path router of APIRouter can accommodate more than one injectable, which is why its 
dependencies parameter always needs a List value ([]).
Dependency injection on routers
However, some transactions are not localized to work on one specific API. There are dependency 
```
[^50]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.86)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.86, lines 4–11)*:
```
The model layer
This layer is purely composed of resources, collections, and Python classes that can be used by the 
repository layer to create CRUD transactions. Some model classes are dependable on other models, 
but some are just independent blueprints designed for data placeholder. Some of the application’s 
model classes that store recipe-related details are shown here:
from uuid import UUID
from model.classifications import Category, Origin
from typing import Optional, List
```
[^51]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Constructor** *(p.73)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.73, lines 7–14)*:
```
FastAPI also allows classes to be injected into any components, since they can also be considered 
callable components. A class becomes callable during instantiation when the call to its constructor, 
__init__(self), is done. Some of these classes have no-arg constructors, while others, such as 
the following Login class, require constructor arguments:
class Login:
    def __init__(self, id: UUID, username: str, 
                 password: str, type: UserType): 
        self.id = id
```
[^52]
**Annotation:** This excerpt demonstrates 'constructor' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.72)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.72, lines 11–18)*:
```
    return account
The function requires the id, username, and password parameters and type to continue its 
process and return a valid JSON account object, derived from these parameters. A dependency 
function sometimes uses some underlying formula, resource, or complex algorithms to derive its 
function value, but for now, we utilize it as a placeholder of data or dict.
Common to dependency functions are method parameters that serve as placeholders to a REST 
API’s incoming request. These are wired into the API’s method parameter list as a domain model to 
the query parameters or request body through DI. The Depends() function from the fastapi 
```
[^53]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Coroutine** *(p.67)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.67, lines 24–31)*:
```
uvicorn main:app --workers 5 --reload
Chapter 8, Creating Coroutines, Events, and Message-Driven Transactions, will discuss the AsyncIO 
platform and the use of coroutines in more detail. 
And now, the last, most important core feature that FastAPI can provide is the middleware or the 
"request-response filter."    
Applying middleware to filter path operations
There are FastAPI components that are inherently asynchronous and one of them is the middleware. 
It is an asynchronous function that acts as a filter for the REST API services. It filters out the incoming 
```
[^54]
**Annotation:** This excerpt demonstrates 'coroutine' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 4: Building the Microservice Application** *(pp.89–130)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^55]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Connecting to a Relational Database** *(pp.131–162)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^56]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Using a Non-Relational Database** *(pp.163–192)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^57]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 4: Building the Microservice Application

*Source: Building Python Microservices with FastAPI, pages 89–130*

### Chapter Summary
Demonstrates building complete microservice applications with proper architectural patterns. Covers layered architecture, repository pattern, service layer design, business logic separation, API controllers, and organizing modular microservice code. [^58]

### Concept-by-Concept Breakdown
#### **None** *(p.120)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.120, lines 2–9)*:
```
97
    mname:Optional[str] = None
    age:Optional[int] = None
    major:Optional[Major] = None
    department:Optional[str] = None
The request models listed in the preceding snippet are just simple BaseModel types. For further 
details on how to create BaseModel classes, Chapter 1, Setting Up FastAPI for Starters, provides 
guidelines for creating different kinds of BaseModel classes to capture different requests from clients.
```
[^59]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.118)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.118, lines 12–19)*:
```
class Assignment: 
    def __init__(self, assgn_id:int, title:str, 
        date_due:datetime, course:str):
        self.assgn_id:int = assgn_id 
        self.title:str = title 
        self.date_completed:datetime = None
        self.date_due:datetime = date_due
        self.rating:float = 0.0 
```
[^60]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.95)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.95, lines 10–17)*:
```
container = Container()
container.wire(modules=[sys.modules[__name__]])
The multiple container setup
For large applications, the number of repository transactions and services increases based on the 
functionality and special features of the application. If the single declarative type becomes unfeasible 
for a growing application, then we can always replace it with a multiple-container setup.
Dependency Injector allows us to create a separate container for each group of services. Our application 
has created a sample setup found in /containers/multiple_containers.py, just in case 
```
[^61]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Repr__** *(p.119)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.119, lines 8–15)*:
```
    
    def __repr__(self): 
        return ' '.join([str(self.bin_id), 
         str(self.stud_id), str(self.faculty_id)])
    def __expr__(self): 
        return ' '.join([str(self.bin_id), 
         str(self.stud_id), str(self.faculty_id)])
These data model classes always have their constructors implemented if constructor injection is needed 
```
[^62]
**Annotation:** This excerpt demonstrates '__repr__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Str__** *(p.119)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.119, lines 15–22)*:
```
These data model classes always have their constructors implemented if constructor injection is needed 
during instantiation. Moreover, the __repr__() and __str__() dunder methods are optionally 
there to provide efficiency for developers when accessing, reading, and logging these objects.
On the other hand, the request models are familiar because they were already discussed in the previous 
chapter. Additionally, the faculty module has the following request models:
class SignupReq(BaseModel):     
    faculty_id:int
    username:str
```
[^63]
**Annotation:** This excerpt demonstrates '__str__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.120)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.120, lines 15–22)*:
```
to optimize and manage data transactions. But aside from the access, this layer provides a high-level 
abstraction for the application so that the specific database technology or dialect used will not matter 
to the applications. It serves as an adapter to any database platform to pursue data transactions for 
the application, nothing else. The following is a repository class of the faculty module, which manages 
the domain for creating assignments for their students:
from fastapi.encoders import jsonable_encoder
from typing import List, Dict, Any
from faculty_mgt.models.data.facultydb import 
```
[^64]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.97)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.97, lines 24–31)*:
```
an object, the container needs its class name as its key and the instance as its value. Moreover, the DI 
framework also allows instantiation with arguments if the constructors require some parameter values.
The FastAPI and Lagom integration
Before the wiring happens, integration to the FastAPI platform must come first by instantiating a 
new API class called FastApiIntegration, which is found in the lagom.integrations.
fast_api module. It takes container as a required parameter:
from lagom.integrations.fast_api import FastApiIntegration
deps = FastApiIntegration(container)
```
[^65]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.121)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.121, lines 3–10)*:
```
    
    def update_assignment(self, assgn_id:int, 
           details:Dict[str, Any]) -> bool: 
       try:
           assignment = faculty_assignments_tbl[assgn_id]
           assignment_enc = jsonable_encoder(assignment)
           assignment_dict = dict(assignment_enc)
           assignment_dict.update(details)         
```
[^66]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 35 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.114)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.114, lines 6–13)*:
```
Using the httpx module
The httpx external module is a Python extension that can consume both asynchronous and 
synchronous REST APIs and has HTTP/1.1 and HTTP/2 support. It is a fast and multi-purpose toolkit 
that is used to access API services running on WSGI-based platforms, as well as, on ASGI, like the 
FastAPI services. But first, we need to install it using pip:
pip install httpx
Then, we can use it directly without further configuration to make two microservices interact, for 
instance, our student module submitting assignments to the faculty module:
```
[^67]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.124)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.124, lines 6–13)*:
```
pydantic’s BaseSettings class.
Storing settings as class attributes
In our architecture setup, it should be the top-level application that will manage the externalized 
values. One way is to store them in a BaseSettings class as attributes. The following are classes 
of the BaseSettings type with their respective application details:
from pydantic import BaseSettings
from datetime import date
class FacultySettings(BaseSettings): 
```
[^68]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.109)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.109, lines 26–33)*:
```
  httptools_impl.py", line 371, in run_asgi
    result = await app(self.scope, self.receive, self.send)
  File "c:\alibata\development\language\python\
  python38\lib\site-packages\uvicorn\middleware\
  proxy_headers.py", line 59, in __call__
    return await self.app(scope, receive, send)
Opting for another logging extension is the only solution to avoid the error generated by the logging 
module. The best option is one that can fully support the FastAPI framework, which is the loguru 
```
[^69]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.101)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.101, lines 20–27)*:
```
by business units and decomposition by subdomains: 
•	 Decomposition by business units is used when the breakdown of the monolithic application is 
based on organizational structures, architectural components, and structural units. Usually, 
its resulting modules have fixed and structured processes and functionality that are seldom 
enhanced or upgraded. 
•	 Decomposition by subdomain uses domain models and their corresponding business processes as 
the basis of the breakdown. Unlike the former, this decomposition strategy deals with modules 
that continuously evolve and change to capture the exact structure of the modules. 
```
[^70]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.90)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.90, lines 4–11)*:
```
factory methods, which are also injectable components but of the service layer. For instance, get_
recipe_repo() will be wired to a service class to pursue the implementation of native services 
that require some transactions from RecipeRepository. In a way, we are indirectly wiring the 
repository class to the service layer.
The service layer
This layer has all the application’s services with the domain logic, such as our RecipeService, which 
provides business processes and algorithms to RecipeRepository. The get_recipe_repo() 
factory is injected through its constructor to provide CRUD transactions from RecipeRepository. 
```
[^71]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.114)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.114, lines 31–32)*:
```
data as parameter values. We use the with context manager to directly manage the streams created by 
its Client() or AsyncClient() instances, which are closeable components.
```
[^72]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.130)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.130, lines 3–10)*:
```
Relational Database
Our previous applications have only used Python collections to hold data records instead of persistent 
data stores. This setup causes data wiping whenever the Uvicorn server restarts because these collections 
only store the data in volatile memory, such as RAM. From this chapter onward, we will be applying 
data persistency to avoid data loss and provide a platform to manage our records, even when the 
server is in shutdown mode.
This chapter will focus on different Object Relational Mappers (ORMs) that can efficiently manage 
clients’ data using objects and a relational database. Object-relational mapping is a technique where 
```
[^73]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 5: Connecting to a Relational Database** *(pp.131–162)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^74]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Using a Non-Relational Database** *(pp.163–192)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^75]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Securing the Backend and API Endpoints** *(pp.193–232)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __repr__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^76]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 5: Connecting to a Relational Database

*Source: Building Python Microservices with FastAPI, pages 131–162*

### Chapter Summary
Focuses on integrating relational databases with FastAPI using SQLAlchemy ORM. Covers database connections, session management, defining database models, migrations with Alembic, implementing CRUD operations, and handling transactions. [^77]

### Concept-by-Concept Breakdown
#### **None** *(p.142)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.142, lines 4–11)*:
```
of records or a single record. The all() function ends the query statement that returns multiple 
records, while first(), scalar(), one(), or one_or_none() can be applied if the result is a 
single row. In get_signup(), one_or_none() is utilized to raise an exception when no record 
is returned. For SQLAlchemy’s query transactions, all these functions can close the Session object. 
The repository classes for SQLAlchemy are in the ch05a folder’s /repository/sqlalchemy/
signup.py module script file.
Creating the JOIN queries
For all the ORMs supported by FastAPI, only SQLAlchemy implements join queries pragmatically 
```
[^78]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.157)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.157, lines 9–16)*:
```
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self._children = set()
    @property
    def children(self):
        return self._children
    @children.setter
```
[^79]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.151)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.151, lines 32–34)*:
```
The ** operator in update_attendance() is a Python operator overload that converts 
a dictionary into kwargs. Thus, the result of **details is a kwargs argument for the 
values() method of the select() directive.
```
[^80]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.141)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.141, lines 4–11)*:
```
filter() first before delete() is called. Another way of implementing this is to retrieve the 
object using sess.query() again and pass the retrieved object as an argument to the Session 
object’s delete(obj), which is a different function. Always remember to invoke commit() to 
flush the changes. Now, the following script shows how to implement the query transactions:
    def get_all_signup(self):
        return self.sess.query(Signup).all() 
    def get_all_signup_where(self, username:str):
        return self.sess.
```
[^81]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.147)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.147, lines 1–8)*:
```
Connecting to a Relational Database
124
Implementing async CRUD transactions using 
SQLAlchemy
From version 1.4, SQLAlchemy supports asynchronous I/O (AsyncIO) features, which enables support 
for asynchronous connections, sessions, transactions, and database drivers. Most of the procedures 
for creating the repository are the same as those for the synchronous setup. The only difference is 
the non-direct access that the CRUD commands have with the asynchronous Session object. Our 
```
[^82]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 44 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.147)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.147, lines 2–9)*:
```
124
Implementing async CRUD transactions using 
SQLAlchemy
From version 1.4, SQLAlchemy supports asynchronous I/O (AsyncIO) features, which enables support 
for asynchronous connections, sessions, transactions, and database drivers. Most of the procedures 
for creating the repository are the same as those for the synchronous setup. The only difference is 
the non-direct access that the CRUD commands have with the asynchronous Session object. Our 
ch05b project showcases the asynchronous side of SQLAlchemy. 
```
[^83]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 25 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.147)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.147, lines 4–11)*:
```
SQLAlchemy
From version 1.4, SQLAlchemy supports asynchronous I/O (AsyncIO) features, which enables support 
for asynchronous connections, sessions, transactions, and database drivers. Most of the procedures 
for creating the repository are the same as those for the synchronous setup. The only difference is 
the non-direct access that the CRUD commands have with the asynchronous Session object. Our 
ch05b project showcases the asynchronous side of SQLAlchemy. 
Installing the asyncio-compliant database drivers
Before we begin setting up the database configuration, we need to install the following asyncio-
```
[^84]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.136)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.136, lines 3–10)*:
```
The Signup class is a sample of a SQLAlchemy model because it inherits the Base class’s properties. 
It is a mapped class because all its attributes are reflections of the column metadata of its physical table 
schema counterpart. The model has a primary_key property set to True because SQLAlchemy 
recommends each table schema have at least one primary key. The rest of the Column objects are 
mapped to column metadata that’s non-primary but can be unique or indexed. Each model class 
inherits the __tablename__ property, which sets the name of the mapped table.
Most importantly, we need to ensure that the data type of the class attribute matches the column type 
of its column counterpart in the table schema. The column attribute must have the same name as the 
```
[^85]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.159)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.159, lines 2–9)*:
```
136
            trainer = await Profile_Trainers.get(id)
            await trainer.update(**details).apply()       
       except: 
           return False 
       return True
Another option is to use the SQLAlchemy ModelClass.update.values(ModelClass).
where(expression) clause, which, when applied to update_trainer(), will give us this 
```
[^86]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.135)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.135, lines 22–29)*:
```
can create model class definitions in SQLAlchemy ORM:
from sqlalchemy import Time, Boolean, Column, Integer, 
    String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from db_config.sqlalchemy_connect import Base
class Signup(Base):
    __tablename__ = "signup"
    id = Column(Integer, primary_key=True, index=True)
```
[^87]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.160)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.160, lines 9–16)*:
```
In the GINO ORM, all queries utilize ModelLoader to load each database record into a model object:
class GymClassRepository:
        
    async def join_classes_trainer(self):
        query = Gym_Class.join(Profile_Trainers).select()
        result = await query.gino.load(Gym_Class.
            distinct(Gym_Class.id).
                load(parent=Profile_Trainers)).all()
```
[^88]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 17 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class Method** *(p.158)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.158, lines 26–33)*:
```
the table in the GINO way involves doing the following: 
•	 First, it requires the get() class method of the model class to retrieve the record object with 
the id primary key.
•	 Second, the extracted record has an instance method called update() that will automatically 
modify the mapped row with the new data specified in its kwargs argument. The apply() 
method will commit the changes and close the transaction:
    async def update_trainer(self, id:int, 
                 details:Dict[str, Any]) -> bool: 
```
[^89]
**Annotation:** This excerpt demonstrates 'class method' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.152)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.152, lines 7–14)*:
```
needs an asynchronous with context manager because of the connection’s AsyncEngine, 
which needs to be closed after every commit() transaction. Closing the session factory is 
not part of the procedure in the synchronous ORM version. 
•	 Second, after its creation, AsyncSession will only start executing all the CRUD transactions 
when the service calls its begin() method. The main reason is that AsyncSession can 
be closed and needs to be closed once the transaction has been executed. That is why another 
asynchronous context manager is used to manage AsyncSession. 
The following code shows the APIRouter script, which implements the services for monitoring 
```
[^90]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.143)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.143, lines 20–27)*:
```
Now, let us apply these repository transactions to the administration-related API services of our 
application. Instead of using collections to store all the records, we will be utilizing the ORM’s transactions 
to manage the data using PostgreSQL. First, we need to import the essential components required by 
the repository, such as SessionFactory, the repository class, and the Signup model class. APIs 
such as Session and other typing APIs can only be part of the implementation for type hints. 
The following script shows a portion of the administrator’s API services highlighting the insertion 
and retrieval services for new access registration:
from fastapi import APIRouter, Depends
```
[^91]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Constructor** *(p.157)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.157, lines 25–32)*:
```
Profile_Members and Gym_Class, and between Login and Profile_Members/Profile_
Trainers. In the previous script, notice the inclusion of a constructor and the custom children 
Python property in Profile_Members, as well as the custom child property in Login. This is 
because GINO only has a built-in parent property.
You can find the domain models of GINO in the /models/data/gino_models.py script.
Important note
@property is a Python decorator that’s used to implement a getter/setter in a class. This 
hides an instance variable from the accessor and exposes its getter and setter property fields. 
```
[^92]
**Annotation:** This excerpt demonstrates 'constructor' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 6: Using a Non-Relational Database** *(pp.163–192)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, args.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^93]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Securing the Backend and API Endpoints** *(pp.193–232)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, args.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^94]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Creating Coroutines, Events, and Message-Driven Transactions** *(pp.233–268)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^95]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 6: Using a Non-Relational Database

*Source: Building Python Microservices with FastAPI, pages 163–192*

### Chapter Summary
Explores non-relational databases including MongoDB and Redis integration. Covers PyMongo usage, document databases, key-value stores, caching strategies, schema-less design, working with collections, and async database operations. [^96]

### Concept-by-Concept Breakdown
#### **None** *(p.172)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.172, lines 12–19)*:
```
from contextvars import ContextVar
db_state_default = {"closed": None, "conn": None, 
         "ctx": None, "transactions": None}
db_state = ContextVar("db_state", 
          default=db_state_default.copy())
class PeeweeConnectionState(_ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
```
[^97]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.172)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.172, lines 17–24)*:
```
class PeeweeConnectionState(_ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)
    def __setattr__(self, name, value):
        self._state.get()[name] = value
    def __getattr__(self, name):
        return self._state.get()[name]
```
[^98]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.170)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.170, lines 31–35)*:
```
      with db_session: 
        generator_args = (m for m in Profile_Members 
              for g in m.gclass)
        joins = left_join(tuple_args)        
        result = [ProfileMembersReq.from_orm(m)
```
[^99]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.184)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.184, lines 2–9)*:
```
Using a Non-Relational 
Database
So far, we have learned that relational databases store data using table columns and rows. All these 
table records are structurally optimized and designed using different keys, such as primary, unique, and 
composite keys. The tables are connected using foreign/reference keys. Foreign key integrity plays a 
significant role in the table relationship of a database schema because it gives consistency and integrity 
to the data that’s persisted in the tables. Chapter 5, Connecting to a Relational Database, provided 
considerable proof that FastAPI can connect to relational databases using any of the present ORMs 
```
[^100]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 30 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.183)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.183, lines 16–23)*:
```
its repository layer. First, there is SQLAlchemy, which provides a boilerplated approach to creating 
standard and asynchronous data persistency and query operations. Then, there is GINO, which uses 
the AsyncIO environment to implement asynchronous CRUD transactions with its handy syntax. 
Also, there is Pony, the most Pythonic among the ORMs presented because it uses hardcore Python 
code to build its repository transactions. Lastly, there is Peewee, known for its concise syntax but 
tricky composition for the asynchronous database connection and CRUD transactions. Each ORM 
has its strengths and weaknesses, but all provide a logical solution rather than applying brute-force 
and native SQL.
```
[^101]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.183)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.183, lines 17–24)*:
```
standard and asynchronous data persistency and query operations. Then, there is GINO, which uses 
the AsyncIO environment to implement asynchronous CRUD transactions with its handy syntax. 
Also, there is Pony, the most Pythonic among the ORMs presented because it uses hardcore Python 
code to build its repository transactions. Lastly, there is Peewee, known for its concise syntax but 
tricky composition for the asynchronous database connection and CRUD transactions. Each ORM 
has its strengths and weaknesses, but all provide a logical solution rather than applying brute-force 
and native SQL.
If the ORM needs fine-tuning, we can add some degree of optimization by using data-related design 
```
[^102]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.166)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.166, lines 10–17)*:
```
    … … … … … …
Defining the relationship attributes depends on the relationship type between the two entities. 
Attributes should be defined as Optional(parent)-Required(child) or Optional(parent)-Optional(child) 
if the relationship type is one-to-one. For one-to-many, attributes should be defined as Set(parent)-
Required(child). Finally, for many-to-one, the attributes must be defined as Set(parent)-Set(child). 
Login has a one-to-one relationship with Profile_Members, which explains the use of the 
Optional attribute to point to the id key of Profile_Members. The primary keys are always 
the reference keys in this relationship for Pony. 
```
[^103]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.163)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.163, lines 8–15)*:
```
async def db_create_tbl():
    engine = await gino.create_engine(DB_URL)
    await GinoSchemaVisitor(metadata).create_all(engine)
As stated in SQLAlchemy, performing DDL transactions such as schema auto-generation at the start 
is optional because it may cause FastAPI’s performance to degrade, and even some conflicts in the 
existing database schema.
Now, let us explore another ORM that requires custom Python coding: Pony ORM. 
Using Pony ORM for the repository layer
```
[^104]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.174)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.174, lines 2–9)*:
```
151
We can’t see any primary keys in the model classes presented because the Peewee engine will create them 
during its schema auto-generation. The physical foreign key column and the model attribute will have 
the same name derived from its model name, with the modelname_id pattern in lowercase form. If 
we insist on adding the primary key for the model, a conflict will occur, making Peewee dysfunctional. 
We must let Peewee create the physical tables from the model classes to avoid this mishap.
All model classes inherit properties from the Model directive of the ORM. It also has column directives 
such as IntegerField, FloatField, DateField, and TimeField for defining the column 
```
[^105]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 12 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class Method** *(p.177)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.177, lines 2–9)*:
```
154
Similarly, the update() class method requires the execute() method after filtering the record 
that needs updating using the id primary key. This is shown in the following code snippet:
    def update_login(self, id:int, 
              details:Dict[str, Any]) -> bool: 
       try:
           query = Login.update(**details).
                  where(Login.id == id)
```
[^106]
**Annotation:** This excerpt demonstrates 'class method' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.189)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.189, lines 3–10)*:
```
    finally:
        client.close()
A generator function such as create_db_collections() is preferred because the yield 
statement works perfectly when it comes to managing the database connection over the return 
statement. The yield statement suspends the function’s execution when it sends a value back to the 
caller but retains the state where the function can resume at the point where it left off. This feature 
is applied by the generator to close the database connection when it resumes the execution at the 
finally clause. The return statement, on the other hand, will not be applicable for this purpose 
```
[^107]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.188)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.188, lines 22–29)*:
```
for example, client["obrs_db"]. Once the database object has been retrieved, we can access 
the collections using the access rules. Note that a collection is equivalent to a table in a relational 
database, where the collated records, known as documents, are stored. The following code shows a 
generator function that’s used by the application to open database connectivity and access the necessary 
collections in preparation for the CRUD implementation:
from pymongo import MongoClient
def create_db_collections():
    client = MongoClient('mongodb://localhost:27017/')
```
[^108]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Comprehension** *(p.169)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.169, lines 30–37)*:
```
following code shows the request model that’s used to extract the records from select() through 
list comprehension and the Profile_Member dict object from get():
from typing import List, Any
from pydantic import BaseModel, validator
class ProfileMembersReq(BaseModel): 
    id: Any
    firstname: str
    lastname: str
```
[^109]
**Annotation:** This excerpt demonstrates 'comprehension' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Constructor** *(p.164)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.164, lines 9–16)*:
```
  user="postgres", password="admin2255", database="fcms")
As you can see, the first parameter of the constructor is the database dialect, followed by kwargs, 
which contains all the details about the connection. The full configuration can be found in the 
/db_config/pony_connect.py script file. Now, let us create Pony's model classes.
Defining the model classes
The created database object, db, is the only component needed to define a Pony entity, a term that refers 
to a model class. It has an Entity attribute, which is used to subclass each model class to provide 
the _table_ attribute, which is responsible for the table-entity mapping. All entity instances are 
```
[^110]
**Annotation:** This excerpt demonstrates 'constructor' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Datetime** *(p.192)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.192, lines 4–11)*:
```
    @validator('date_shipped')
    def date_shipped_datetime(cls, value):
        return datetime.strptime(value, 
           "%Y-%m-%dT%H:%M:%S").date()
    
    @validator('date_payment')
    def date_payment_datetime(cls, value):
        return datetime.strptime(value, 
```
[^111]
**Annotation:** This excerpt demonstrates 'datetime' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 7: Securing the Backend and API Endpoints** *(pp.193–232)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, args.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^112]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Creating Coroutines, Events, and Message-Driven Transactions** *(pp.233–268)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^113]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Utilizing Other Advanced Features** *(pp.269–300)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, args.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^114]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 7: Securing the Backend and API Endpoints

*Source: Building Python Microservices with FastAPI, pages 193–232*

### Chapter Summary
Addresses security concerns for FastAPI applications including authentication and authorization mechanisms. Covers OAuth2 implementation, JWT tokens, password hashing with bcrypt, CORS configuration, API keys, and bearer token authentication. [^115]

### Concept-by-Concept Breakdown
#### **None** *(p.195)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.195, lines 2–9)*:
```
172
    shipping_address: Optional[str] = None
    email: Optional[str] = None   
    date_purchased: Optional[date] = "1900-01-01T00:00:00"
    date_shipped: Optional[date] = "1900-01-01T00:00:00"
    date_payment: Optional[date] = "1900-01-01T00:00:00"
    
    @validator('date_purchased', pre=True)
```
[^116]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.196)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.196, lines 15–22)*:
```
             "%Y-%m-%dT%H:%M:%S").date()
@dataclass is a decorator function that adds an __init__() to a Python class to initialize 
its attributes and other special functions, such as __repr__(). The PurchasedHistory, 
PurchaseStatus, and Buyer custom classes shown in the preceding code are typical classes that 
can be converted into request model classes. FastAPI supports both BaseModel and data classes when 
creating model classes. Apart from being under the Pydantic module, using @dataclass is not a 
replacement for using BaseModel when creating model classes. This is because the two components 
are different in terms of their flexibility, features, and hooks. BaseModel is configuration-friendly 
```
[^117]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Repr__** *(p.196)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.196, lines 16–23)*:
```
@dataclass is a decorator function that adds an __init__() to a Python class to initialize 
its attributes and other special functions, such as __repr__(). The PurchasedHistory, 
PurchaseStatus, and Buyer custom classes shown in the preceding code are typical classes that 
can be converted into request model classes. FastAPI supports both BaseModel and data classes when 
creating model classes. Apart from being under the Pydantic module, using @dataclass is not a 
replacement for using BaseModel when creating model classes. This is because the two components 
are different in terms of their flexibility, features, and hooks. BaseModel is configuration-friendly 
and can be adapted to many validation rules and type hints, while @dataclass has problems 
```
[^118]
**Annotation:** This excerpt demonstrates '__repr__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.231)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.231, lines 10–17)*:
```
    _collection = "reference"
A Frame model class can wrap a document in dictionary form or in a kwargs that contains the 
key-value details of the document’s structure. It can also provide attributes and helper methods that 
can help pursue CRUD transactions. All the fields of the model class can be accessed through dot (.) 
notation, just like typical class variables.
Creating the document association
We need to define the SubFrame model before creating associations among these documents. A 
SubFrame model class is mapped to an embedded document structure and has no collection table 
```
[^119]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.227)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.227, lines 17–24)*:
```
When fetching a single document so that it can be updated or deleted, AIOEngine has a find_
one() method that requires two arguments: the model class name and the conditional expression, 
which involves either the id primary key or some non-unique fields. All the fields can be accessed 
like class variables. The following get_purchase() method retrieves a Purchase document 
with the specified id:
    async def get_all_purchase(self):
        purchases = await self.engine.find(Purchase)
        return purchases
```
[^120]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.196)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.196, lines 3–10)*:
```
    user_id: int 
    date_purchased: date 
    purchase_history: List[PurchaseHistory] = 
          field(default_factory=list )
    customer_status: Optional[PurchaseStatus] = 
          field(default_factory=dict)
    _id: ObjectId = field(default=ObjectId())
    
```
[^121]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 35 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.205)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.205, lines 17–24)*:
```
using the MongoDB server. However, the driver only works for synchronous CRUD transactions. If 
we opt for an asynchronous way of implementing CRUD, we must always resort to the Motor driver.
Creating async CRUD transactions using Motor
Motor is an asynchronous driver that relies on the AsyncIO environment of the FastAPI. It wraps 
PyMongo to produce non-blocking and coroutine-based classes and methods needed to create 
asynchronous repository layers. It is almost like PyMongo when it comes to most of the requirements 
except for the database connectivity and repository implementation.
But before we proceed, we need to install the motor extension using the following pip command:
```
[^122]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 12 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.205)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.205, lines 19–26)*:
```
Creating async CRUD transactions using Motor
Motor is an asynchronous driver that relies on the AsyncIO environment of the FastAPI. It wraps 
PyMongo to produce non-blocking and coroutine-based classes and methods needed to create 
asynchronous repository layers. It is almost like PyMongo when it comes to most of the requirements 
except for the database connectivity and repository implementation.
But before we proceed, we need to install the motor extension using the following pip command:
pip install motor
Setting up the database connectivity
```
[^123]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.211)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.211, lines 21–28)*:
```
        return cls(**json_dict)
Unlike PyMongo and the Motor drivers, MongoEngine can define class attributes using its Field 
classes and their properties. Some of its Field classes include StringField, IntField, 
FloatField, BooleanField, and DateField. These can declare the str, int, float, 
bool, and datetime.date class attributes, respectively. 
Another convenient feature that this ODM has is that it can create SequenceField, which behaves 
the same as the auto_increment column field in a relational database or Sequence in an 
object-relational database. The id field of a model class should be declared as SequenceField so 
```
[^124]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.222)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.222, lines 2–9)*:
```
199
          cart = await Cart.get(id)
          await cart.set({Cart.qty:qty})
       except: 
           return False 
       return True
    
    async def delete_item(self, id:int) -> bool: 
```
[^125]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.211)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.211, lines 23–30)*:
```
classes and their properties. Some of its Field classes include StringField, IntField, 
FloatField, BooleanField, and DateField. These can declare the str, int, float, 
bool, and datetime.date class attributes, respectively. 
Another convenient feature that this ODM has is that it can create SequenceField, which behaves 
the same as the auto_increment column field in a relational database or Sequence in an 
object-relational database. The id field of a model class should be declared as SequenceField so 
that it serves as the primary key of the document. Like in a typical sequence, this field has utilities to 
increment its value or reset it to zero, depending on what document record must be accessed. 
```
[^126]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.196)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.196, lines 15–22)*:
```
             "%Y-%m-%dT%H:%M:%S").date()
@dataclass is a decorator function that adds an __init__() to a Python class to initialize 
its attributes and other special functions, such as __repr__(). The PurchasedHistory, 
PurchaseStatus, and Buyer custom classes shown in the preceding code are typical classes that 
can be converted into request model classes. FastAPI supports both BaseModel and data classes when 
creating model classes. Apart from being under the Pydantic module, using @dataclass is not a 
replacement for using BaseModel when creating model classes. This is because the two components 
are different in terms of their flexibility, features, and hooks. BaseModel is configuration-friendly 
```
[^127]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 16 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class Method** *(p.194)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.194, lines 2–9)*:
```
171
@validator creates a class method that accepts class name as the first parameter, not the 
instance, of the field(s) to be validated and parsed. Its second parameter is an option that specifies 
the field name or class attribute that needs to be converted into another data type, such as date_
purchased, date_shipped, or date_payment of the PurchaseRequestReq model. The 
pre attribute of @validator tells FastAPI to process the class methods before any built-in validation 
can be done in the API service implementation. These methods are executed right after APIRouter 
runs its custom and built-in FastAPI validation rules for the request models, if there are any.
```
[^128]
**Annotation:** This excerpt demonstrates 'class method' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.206)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.206, lines 7–14)*:
```
    return {"users": users, "buyers": buyers}
def close_async_db(): 
    client.close()
The format of the database URI is a string with a colon (:) in between the details. Now, the application 
needs the following Motor methods to start the database transactions: 
•	 create_async_db(): A method for establishing the database connection and loading 
schema definitions
•	 close_async_db(): A method for closing the connection
```
[^129]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.206)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.206, lines 2–9)*:
```
183
def create_db_collections():
    db = client.obrs
    buyers = db["buyer"]
    users = db["login"]
    return {"users": users, "buyers": buyers}
def close_async_db(): 
    client.close()
```
[^130]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 8: Creating Coroutines, Events, and Message-Driven Transactions** *(pp.233–268)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^131]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Utilizing Other Advanced Features** *(pp.269–300)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, args.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^132]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: Solving Numerical, Symbolic, and Graphical Problems** *(pp.301–328)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^133]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 8: Creating Coroutines, Events, and Message-Driven Transactions

*Source: Building Python Microservices with FastAPI, pages 233–268*

### Chapter Summary
Examines asynchronous programming with coroutines, asyncio, and event-driven architecture. Covers background tasks, message queues, Celery integration, RabbitMQ and Kafka messaging, implementing producers and consumers, and event-driven transaction patterns. [^134]

### Concept-by-Concept Breakdown
#### **None** *(p.254)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.254, lines 3–10)*:
```
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    loginrepo = LoginRepository(sess)
```
[^135]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.243)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.243, lines 24–31)*:
```
        bytes(f"{config['USERNAME']}:{config['PASSWORD']}",
           encoding="UTF-8")
    )
    is_credentials = compare_digest(
          bytes(hashed_credentials, encoding="UTF-8"),
               expected_credentials)
    
    if not is_credentials:
```
[^136]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.254)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.254, lines 30–36)*:
```
class OAuth2PasswordBearerScopes(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
```
[^137]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.233)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.233, lines 4–11)*:
```
which extracts all BSON documents, and the one() method, which returns a single document object. 
Both operations can accept a query expression as an argument if there are any constraints. Moreover, 
MongoFrames has a Q query maker class that’s used to build conditionals in a query expression. The 
expression starts with Q, followed by dot (.) notation to define the field name or path – for example, 
Q.categories.fiction – followed by an operator (for example, ==, !=, >, >=, <, or <=) and 
finally a value. The following code shows examples of the query transactions being translated using 
the MongoFrames ODM syntax:
    def get_all_book(self):
```
[^138]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.238)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.238, lines 1–8)*:
```
Implementing Basic and Digest authentication
215
http_basic = HTTPBasic()
The FastAPI framework supports different authentication modes and specifications through its 
fastapi.security module. To pursue the Basic authentication scheme, we need to instantiate 
the HTTPBasic class of the module and inject it into each API service to secure the endpoint access. 
The http_basic instance, once injected into the API services, causes the browser to pop up a login 
form, through which we type the username and password credentials. Logging in will trigger 
```
[^139]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 33 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.255)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.255, lines 10–17)*:
```
       scheme_name=scheme_name, auto_error=auto_error)
    async def __call__(self, request: Request) -> 
             Optional[str]:
        header_authorization: str = 
              request.headers.get("Authorization")
        … … … … … …
        return param
This OAuth2PasswordBearerScopes class requires two constructor parameters, tokenUrl 
```
[^140]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.233)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.233, lines 23–30)*:
```
As explained earlier, adding embedded documents is determined by the operation and not by the 
model attributes. In the following add_category() transaction, it is clear that a Category object 
has been assigned to a category field of a Book instance, even if the field is not defined to refer 
to an embedded document of the Category type. Instead of throwing an exception, MongoFrame 
will update the Book document right after the update() call:
    def add_category(self, id:int, 
               category:Category) -> bool: 
       try:
```
[^141]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.254)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.254, lines 24–31)*:
```
user authorization. 
Customizing the OAuth2 class
First, we need to create a custom class that inherits the properties of the OAuth2 API class from 
the fastapi.security module to include the scopes parameter or "role" options in the user 
credentials. The following is the OAuth2PasswordBearerScopes class, a custom OAuth2 class 
that will implement the authentication flow with authorization:
class OAuth2PasswordBearerScopes(OAuth2):
    def __init__(
```
[^142]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class Method** *(p.233)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.233, lines 2–9)*:
```
210
When creating query transactions, the Frame API provides two class methods – the many() method, 
which extracts all BSON documents, and the one() method, which returns a single document object. 
Both operations can accept a query expression as an argument if there are any constraints. Moreover, 
MongoFrames has a Q query maker class that’s used to build conditionals in a query expression. The 
expression starts with Q, followed by dot (.) notation to define the field name or path – for example, 
Q.categories.fiction – followed by an operator (for example, ==, !=, >, >=, <, or <=) and 
finally a value. The following code shows examples of the query transactions being translated using 
```
[^143]
**Annotation:** This excerpt demonstrates 'class method' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.250)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.250, lines 16–22)*:
```
Moreover, you will notice that all padlock icons of the secured API endpoints that include /ch07/
auctions/add, shown in Figure 7.6, are closed. This indicates that they are ready to be executed 
since the user is already an authenticated one:
Figure 7.6 – An OpenAPI dashboard showing secured APIs
This solution is a problem for an open network setup, for instance, because the token used is a password. 
This setup allows attackers to easily forge or modify the token during its transmission from the issuer 
to the client. One way to protect the token is to use a JSON Web Token (JWT).
```
[^144]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Constructor** *(p.255)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.255, lines 16–23)*:
```
        return param
This OAuth2PasswordBearerScopes class requires two constructor parameters, tokenUrl 
and scopes, to pursue an auth flow. OAuthFlowsModel defines the scopes parameter as part 
of the user credentials for authentication using the Authorization header.
Building the permission dictionary
Before we proceed with the auth implementation, we need to first build the scopes parameters 
that the OAuth2 scheme will be applying during authentication. This setup is part of the 
OAuth2PasswordBearerScopes instantiation, where we assign these parameters to its scopes 
```
[^145]
**Annotation:** This excerpt demonstrates 'constructor' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.253)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.253, lines 9–16)*:
```
If the token is tampered with, modified, or expired, the method will throw an change to - exception. 
Otherwise, we need to continue the payload data extraction, retrieve the username, and store that in an 
@dataclass instance, such as TokenData. Then, the username will undergo further verification, 
such as checking the database for a Login account with that username. The following snippet shows 
this decoding process, found in the /security/secure.py module of the ch07d project:
from models.request.tokens import TokenData
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
```
[^146]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Datetime** *(p.251)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.251, lines 26–33)*:
```
from jose import jwt, JWTError
from datetime import datetime, timedelta
SECRET_KEY = "tbWivbkVxfsuTxCP8A+Xg67LcmjXXl/sszHXwH+TX9w="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_access_token(data: dict, 
           expires_after: timedelta):
    plain_text = data.copy()
```
[^147]
**Annotation:** This excerpt demonstrates 'datetime' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.233)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.233, lines 6–13)*:
```
MongoFrames has a Q query maker class that’s used to build conditionals in a query expression. The 
expression starts with Q, followed by dot (.) notation to define the field name or path – for example, 
Q.categories.fiction – followed by an operator (for example, ==, !=, >, >=, <, or <=) and 
finally a value. The following code shows examples of the query transactions being translated using 
the MongoFrames ODM syntax:
    def get_all_book(self):
        books = [b.to_json_type() for b in Book.many()]
        return books
```
[^148]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Dictionary** *(p.255)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.255, lines 19–26)*:
```
of the user credentials for authentication using the Authorization header.
Building the permission dictionary
Before we proceed with the auth implementation, we need to first build the scopes parameters 
that the OAuth2 scheme will be applying during authentication. This setup is part of the 
OAuth2PasswordBearerScopes instantiation, where we assign these parameters to its scopes 
parameter. The following script shows how all the custom-defined user scopes are saved in a dictionary, 
with the keys as the scope names and the values as their corresponding descriptions:
oauth2_scheme = OAuth2PasswordBearerScopes(
```
[^149]
**Annotation:** This excerpt demonstrates 'dictionary' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 9: Utilizing Other Advanced Features** *(pp.269–300)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^150]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: Solving Numerical, Symbolic, and Graphical Problems** *(pp.301–328)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^151]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Adding Other Microservice Features** *(pp.329–360)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^152]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 9: Utilizing Other Advanced Features

*Source: Building Python Microservices with FastAPI, pages 269–300*

### Chapter Summary
Covers advanced FastAPI features including custom middleware, CORS configuration, WebSocket support, GraphQL integration, file uploads, streaming responses, exception handlers, custom configurations, logging, and Jinja2 template rendering. [^153]

### Concept-by-Concept Breakdown
#### **None** *(p.283)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.283, lines 6–13)*:
```
            else:
                assigned_billing['billing_items'] = None
            
            await q.put(assigned_billing)
    async def build_billing_sheet(q: Queue):
        while True: 
            await asyncio.sleep(2)
            assigned_billing = await q.get()
```
[^154]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.297)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.297, lines 3–10)*:
```
                     messenger_dict = 
                      json.loads(rec.value.decode('utf-8'),
                       object_hook=date_hook_deserializer )
                                             
                     repo = MessengerRepository()
                     result = await 
                      repo.insert_messenger(messenger_dict)
                     id = uuid4()
```
[^155]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.273)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.273, lines 29–36)*:
```
class UsernameAuthBackend(AuthenticationBackend):
    def __init__(self, username): 
        self.username = username    
        
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return
        auth = request.headers["Authorization"]
```
[^156]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.288)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.288, lines 11–18)*:
```
celery.config_from_object(CeleryConfig)
celery_log = get_task_logger(__name__)
To create the Celery instance, we need the following details:
•	 The name of the current module containing the Celery instance (the first argument)
•	 The URL of Redis as our message broker (broker)
•	 The backend result where the results of tasks are stored and monitored (backend)
•	 The list of other modules used in the message body or by the Celery task (include)
After the instantiation, we need to set the appropriate serializer and content types to process the incoming 
```
[^157]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.290)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.290, lines 7–14)*:
```
optimize the task execution. These details are queue, time_limit, retry, ignore_result, 
expires, and some kwargs of arguments. But both these functions return an AsyncResult 
object, which returns resources such as the task’s state, the wait() function to help the task finish 
its operation, and the get() function to return its computed value or an exception. The following 
code is a coroutine API service that calls the services.billing.tasks.create_total_
payables_year_celery task using the apply_async method:
@router.post("/billing/total/payable")
async def compute_payables_yearly(billing_date:date):
```
[^158]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.285)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.285, lines 27–34)*:
```
the background task will use the event loop instead of waiting for the current thread to finish its jobs.
If the background process requires arguments, we pass these arguments to add_task() right after its 
first parameter. For instance, the arguments for the billing_date and query_list parameters 
of generate_billing_sheet() should be placed after the generate_billing_sheet 
injection into add_task(). Moreover, the billing_date value should be passed before 
the result argument because add_task() still follows the order of parameter declaration in 
generate_billing_sheet() to avoid a type mismatch.
All asynchronous background tasks will continuously execute and will not be awaited even if their 
```
[^159]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.290)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.290, lines 1–8)*:
```
Understanding Celery tasks
267
Calling the task
FastAPI services can call these tasks using the apply_async()or delay()function. The latter 
is the easier option since it is preconfigured and only needs the parameters for the transaction to get 
the result. The apply_async() function is a better option since it accepts more details that can 
optimize the task execution. These details are queue, time_limit, retry, ignore_result, 
expires, and some kwargs of arguments. But both these functions return an AsyncResult 
```
[^160]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 33 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.279)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.279, lines 2–9)*:
```
256
A coroutine function can invoke and await multiple coroutines concurrently using the asyncio.
gather() utility. This asyncio method manages a list of coroutines and waits until all its 
coroutines have completed their tasks. Then, it will return a list of results from the corresponding 
coroutines. The following code is an API that retrieves login records through an asynchronous CRUD 
transaction and then invokes count_login() and build_user_list() concurrently to 
process these records:
@router.get("/login/list/records")
```
[^161]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 14 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.278)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.278, lines 2–9)*:
```
255
Applying @asyncio.coroutine 
asyncio is a Python extension that implements the Python concurrency paradigm using a single-
threaded and single-process model and provides API classes and methods for running and managing 
coroutines. This extension provides an @asyncio.coroutine decorator that transforms API 
and native services into generator-based coroutines. However, this is an old approach and can only be 
used in FastAPI that uses Python 3.9 and below. The following is a login service transaction of our 
newsstand management system prototype implemented as a coroutine:
```
[^162]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.289)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.289, lines 7–14)*:
```
composed of the package, module name(s), and the method name of the transaction. It has other 
attributes that can add more refinement to the task definition, such as the auto_retry list, which 
registers Exception classes that may cause execution retries when emitted, and max_tries, 
which limits the number of retry executions of a task. By the way, Celery 5.2.3 and below can only 
define tasks from non-coroutine methods. 
The services.billing.tasks.create_total_payables_year_celery task shown 
here adds all the payable amounts per date and returns the total amount:
@celery.task(
```
[^163]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.281)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.281, lines 13–20)*:
```
    repo = AdminLoginRepository()
    result = await repo.join_login_admin()
    encoded_data = await asyncio.gather(
       *(extract_enc_admin_profile(rec) for rec in result))
    return encoded_data
Now, the extract_enc_admin_profile() coroutine, shown in the following code, implements 
a chaining design pattern, where it calls the other smaller coroutines through a chain. Simplifying and 
breaking down the monolithic and complex processes into smaller but more robust coroutines will 
```
[^164]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.281)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.281, lines 19–26)*:
```
a chaining design pattern, where it calls the other smaller coroutines through a chain. Simplifying and 
breaking down the monolithic and complex processes into smaller but more robust coroutines will 
improve the application’s performance by utilizing more context switches. In this API, extract_
enc_admin_profile() creates three context switches in a chain, better than thread switches:
async def extract_enc_admin_profile(admin_rec):
    p = await extract_profile(admin_rec)
    pinfo = await extract_condensed(p)
    encp = await decrypt_profile(pinfo)
```
[^165]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.273)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.273, lines 12–19)*:
```
ch07h project has these details stored in the app.env file to be retrieved by its get_current_
user() for the payload generation. But then again, the HTTPBearer class needs an auth_token 
from executing the following Okta’s tokenURL, based on the account’s issuer:
curl --location --request POST "https://dev-5180227.
okta.com/oauth2/default/v1/token?grant_type=client_
credentials&client_id=0oa3tvejee5UPt7QZ5d7&client_
secret=LA4WP8lACWKu4Ke9fReol0fNSUvxsxTvGLZdDS5-"   --header 
"Content-Type: application/x-www-form-urlencoded"
```
[^166]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.299)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.299, lines 12–19)*:
```
           {}.".format(client_resp['rec_id']))
    await websocket.close()    
First, we decorate a coroutine function with @router.websocket() when using APIRouter, or 
@api.websocket() when using the FastAPI decorator to declare a WebSocket component. The 
decorator must also define a unique endpoint URL for the WebSocket. Then, the WebSocket function 
must have an injected WebSocket as its first method argument. It can also include other parameters 
such as query and header parameters.
The WebSocket injectable has four ways for sending messages, namely send(), send_text(), 
```
[^167]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Constructor** *(p.274)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.274, lines 13–20)*:
```
             SimpleUser(username)
Activating this UsernameAuthBackend means injecting it into the FastAPI constructor in 
main.py with AuthenticationMiddleware. It also needs the designated username for its 
authentication process to work. The following snippet shows how to activate the whole authentication 
scheme in the main.py file:
from security.secure import UsernameAuthBackend
from starlette.middleware import Middleware
from starlette.middleware.authentication import 
```
[^168]
**Annotation:** This excerpt demonstrates 'constructor' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 10: Solving Numerical, Symbolic, and Graphical Problems** *(pp.301–328)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^169]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Adding Other Microservice Features** *(pp.329–360)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^170]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 12: Deploying FastAPI Applications in the Cloud** *(pp.361–386)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^171]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 10: Solving Numerical, Symbolic, and Graphical Problems

*Source: Building Python Microservices with FastAPI, pages 301–328*

### Chapter Summary
Demonstrates integrating scientific computing libraries with FastAPI for numerical, symbolic, and graphical problems. Covers NumPy for calculations, Pandas for data analysis, Matplotlib for visualization, dataframes, and serving computational results via APIs. [^172]

### Concept-by-Concept Breakdown
#### **None** *(p.305)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.305, lines 22–29)*:
```
async def convert_str(rec):
    if not rec == None:
        total = rec['qty'] * rec['price']
        record = " ".join([rec['branch'], 
            str(total), rec['date_purchased']])
        await asyncio.sleep(1)
        return record
Running these two functions modifies the original emitted data stream from JSON to a date-filtered 
```
[^173]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.324)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.324, lines 4–11)*:
```
        body = await super().body()
        login_dict = ast.literal_eval(body.decode('utf-8'))
        fernet = Fernet(bytes(login_dict['key'], 
             encoding='utf-8'))
        data = fernet.decrypt(
          bytes(login_dict['enc_login'], encoding='utf-8'))
        self.state.dec_data = json.loads(
             data.decode('utf-8'))
```
[^174]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.316)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.316, lines 15–22)*:
```
class SessionDbMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, sess_key: str, 
                    sess_name:str, expiry:str):
        super().__init__(app)
        self.sess_key = sess_key
        self.sess_name = sess_name 
        self.expiry = expiry
        self.client_od = 
```
[^175]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.303)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.303, lines 7–14)*:
```
•	 An on_error() method to flag an error during the subscription process
And since the Observable processes run asynchronously, the scheduler is an optional argument 
that provides the right manager to schedule and run these processes. The API service used 
AsyncIOScheduler as the appropriate schedule for the subscription. But there are other shortcuts 
to generating Observables that do not use a custom function.
Creating background process
As when we create continuously running Observables, we use the interval() function instead of 
using a custom Observable function. Some observables are designed to end successfully, but some 
```
[^176]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.307)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.307, lines 4–11)*:
```
Meanwhile, the shutdown event cleans up unwanted memory, destroys unwanted connections, and logs 
the reason for shutting down the application. The following is the shutdown event of our application 
that closes the GINO database connection:
@app.on_event("shutdown")
async def destroy():
    engine, db.bind = db.bind, None
    await engine.close()
We can define startup and shutdown events in APIRouter but be sure this will not cause transaction 
```
[^177]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 25 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.307)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.307, lines 7–14)*:
```
@app.on_event("shutdown")
async def destroy():
    engine, db.bind = db.bind, None
    await engine.close()
We can define startup and shutdown events in APIRouter but be sure this will not cause transaction 
overlapping or collision with other routers. Moreover, event handlers do not work in mounted 
sub-applications.
Summary
```
[^178]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.302)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.302, lines 3–10)*:
```
Our process_list() emits the details of the publication that gained some profit. Then, we create 
an asyncio task for the call of the process_list() coroutine. We created a nested function, 
evaluate_profit(), which returns the Disposable task required by RxPY’s create() 
method for the production of the Observable stream. The cancellation of this task happens when 
the Observable stream is all consumed. The following is the complete implementation for the 
execution of the asynchronous Observable function and the use of the create() method to 
generate streams of data from this Observable function:
def create_observable(loop):
```
[^179]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.323)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.323, lines 5–12)*:
```
The overridden form() method of ExtractionRequest is responsible for the user_details 
attribute containing all the user details.
On the other hand, the given set_ratings() method has an incoming dictionary of various 
ratings in which the json() override will derive some basic statistics. All the results will be returned 
as Request’s state objects or request attributes:
@router.post("/rating/top/three")
async def set_ratings(req: Request, data : 
 Dict[str, float], user: str = Depends(get_current_user)):
```
[^180]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.317)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.317, lines 6–13)*:
```
               
                login = await repo_login.
                  get_login_credentials(username, password)
               
                if login == None:
                    self.client_od.close()
                    return JSONResponse(status_code=403) 
                else:
```
[^181]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.305)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.305, lines 8–15)*:
```
    return observable
The filter() method is another pipeline operator that returns Boolean values from a validation 
rule. It executes the following filter_within_dates() to verify whether the record retrieved 
from the JSON document is within the date range specified by the subscriber:
def filter_within_dates(rec, min_date:date, max_date:date):
    date_pur = datetime.strptime(
             rec['date_purchased'], '%Y-%m-%d')
    if date_pur.date() >= min_date and 
```
[^182]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.326)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.326, lines 10–17)*:
```
            if disconnected:
                break
            yield 'data: {}\n\n.format(
               json.dumps(jsonable_encoder(q), 
                      cls=MyJSONEncoder))
            await asyncio.sleep(1)
    return StreamingResponse(print_questions(), 
                media_type="text/event-stream")
```
[^183]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.328)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.328, lines 7–14)*:
```
        <body>
          <div class="container">
            <h2>Sign Up Form</h2>
            <form>
                <div class="form-group">
                   <label for="firstname">
                          Firstname:</label>
                   <input type='text' 
```
[^184]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.307)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.307, lines 5–12)*:
```
the reason for shutting down the application. The following is the shutdown event of our application 
that closes the GINO database connection:
@app.on_event("shutdown")
async def destroy():
    engine, db.bind = db.bind, None
    await engine.close()
We can define startup and shutdown events in APIRouter but be sure this will not cause transaction 
overlapping or collision with other routers. Moreover, event handlers do not work in mounted 
```
[^185]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Closure** *(p.321)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.321, lines 7–14)*:
```
        return custom_route_handler
Customizing APIRoute requires the creation of a Python closure that will directly manage the 
Request and Response flow from APIRoute’s original_route_handler. On the other 
hand, our ExtractContentRoute filter uses a custom ExtractionRequest that identifies 
and processes each type of incoming request data separately. The following is the implementation of 
ExtractionRequest that will replace the default Request object: 
class ExtractionRequest(Request):
    async def body(self):
```
[^186]
**Annotation:** This excerpt demonstrates 'closure' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Constructor** *(p.314)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.314, lines 13–20)*:
```
instance of FastAPI is located because APIRouter cannot add middleware. We enable the 
middleware parameter of the FastAPI constructor and add to that List-type parameter the built-in 
SessionMiddleware with its secret_key and the name of the new session as constructor 
parameters using the injectable class, Middleware. The following code snippet of main.py shows 
you how to configure this:
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI(middleware=[
        Middleware(SessionMiddleware, 
```
[^187]
**Annotation:** This excerpt demonstrates 'constructor' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 11: Adding Other Microservice Features** *(pp.329–360)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^188]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 12: Deploying FastAPI Applications in the Cloud** *(pp.361–386)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^189]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 13: Converting APIs and Microservices** *(pp.387–404)*

This later chapter builds upon the concepts introduced here, particularly: None, as, async.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^190]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 11: Adding Other Microservice Features

*Source: Building Python Microservices with FastAPI, pages 329–360*

### Chapter Summary
Explores additional microservice features including caching with Redis, rate limiting and throttling, pagination strategies, API versioning, health check endpoints, monitoring solutions, logging practices, and OpenAPI/Swagger documentation. [^191]

### Concept-by-Concept Breakdown
#### **None** *(p.345)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.345, lines 8–15)*:
```
      "login_id": 101,  
      "password":"sjctrags", "passphrase": None, 
      "profile": None})
app.dependency_overrides[get_current_user] =  get_user
def test_rating_top_three():
    response = client.post("/ch09/rating/top/three", 
     json={
          "rate1": 10.0, 
```
[^192]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.331)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.331, lines 8–15)*:
```
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" 
              content="IE=edge">
        <meta name="viewport" content="width=device-width, 
             initial-scale=1.0, shrink-to-fit=no">
        <meta name="apple-mobile-web-app-capable" 
             content="yes">
```
[^193]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.357)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.357, lines 15–22)*:
```
which deals with data analysis and manipulation using numpy, scipy, and pandas.
Creating arrays and DataFrames
When numerical algorithms require some arrays to store data, a module called NumPy, short for 
Numerical Python, is a good resource for utility functions, objects, and classes that are used to create, 
transform, and manipulate arrays.
The module is best known for its n-dimensional arrays or ndarrays, which consume less memory storage 
than the typical Python lists. An ndarray incurs less overhead when performing data manipulation 
than executing the list operations in totality. Moreover, ndarray is strictly heterogeneous, unlike 
```
[^194]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.344)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.344, lines 2–9)*:
```
321
Writing the unit test cases
It is a best practice to write one test module per router component, except for cases where there is a 
tight connection between these routers. We place these test modules inside the test directory. To 
pursue the automated testing, we need to import the APIRouter instance or the FastAPI instance 
into the test module to set up TestClient. TestClient is almost like Python’s client module, 
requests, when it comes to the helper methods used to consume APIs.
The method names of the test cases must start with a test_ prefix, which is a pytest requirement. 
```
[^195]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 21 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.344)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.344, lines 17–24)*:
```
    response = client.get("/restaurant/index")
    assert response.status_code == 200
    assert response.text == "The Restaurants"
TestClient supports assert statements that check the response of its helper methods, like get(), 
post(), put(), and delete() the status code and response body of the API. The test_
restaurant_index(), for instance, uses the get() method of the TestClient API to run /
restaurant/index GET service and extract its response. The assert statements are used if the 
statuc_code and response.text are correct. The endpoint has no imposed dependencies, 
```
[^196]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.346)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.346, lines 11–18)*:
```
MongoDB connectivity to access the list of login profiles. For the test to work, we need to create a 
mock AsyncIOMotorClient object with a dummy test database called orrs_test. Here is the 
test_list_login() test, which implements this database mocking:
def db_connect():
    client_od = 
         AsyncIOMotorClient(f"mongodb://localhost:27017/")
    engine = AIOEngine(motor_client=client_od, 
            database="orrs_test")
```
[^197]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.346)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.346, lines 11–18)*:
```
MongoDB connectivity to access the list of login profiles. For the test to work, we need to create a 
mock AsyncIOMotorClient object with a dummy test database called orrs_test. Here is the 
test_list_login() test, which implements this database mocking:
def db_connect():
    client_od = 
         AsyncIOMotorClient(f"mongodb://localhost:27017/")
    engine = AIOEngine(motor_client=client_od, 
            database="orrs_test")
```
[^198]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.338)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.338, lines 8–15)*:
```
When adding documentation to the API endpoints, the path operators of FastAPI and APIRouter 
also have parameters that allow changes to the default OpenAPI variables attributed to each endpoint. The 
following is a sample service that updates its summary, description, response_description, 
and other response details through the post() path operator:
@router.post("/restaurant/add",
     summary="This API adds new restaurant details.",
     description="This operation adds new record to the 
          database. ",
```
[^199]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.333)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.333, lines 4–11)*:
```
    repo:LoginRepository = LoginRepository(engine)
    result = await repo.get_all_login()
    return templates.TemplateResponse("users.html", 
           {"request": req, "data": result})
Using ORJSONResponse and UJSONResponse
When it comes to yielding numerous dictionaries or JSON-able-components, it is appropriate to use 
either ORJSONResponse or UJSONResponse. ORJSONResponse uses orjson to serialize a 
humongous listing of dictionary objects into a JSON string as a response. So, first, we need to install 
```
[^200]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.352)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.352, lines 14–21)*:
```
from piccolo.columns import ForeignKey, Integer, Varchar,
       Text, Date, Boolean, Float
from piccolo.table import Table
class Login(Table):
    username = Varchar(unique=True)
    password = Varchar()
class Education(Table):
    name = Varchar()
```
[^201]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.352)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.352, lines 10–17)*:
```
Like in Django ORM, Piccolo ORM has migration commands to generate the database tables based 
on model classes. But first, we need to create model classes by utilizing its Table API class. It also 
has helper classes to establish column mappings and foreign key relationships. The following are some 
data model classes that comprise our database pccs:
from piccolo.columns import ForeignKey, Integer, Varchar,
       Text, Date, Boolean, Float
from piccolo.table import Table
class Login(Table):
```
[^202]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.357)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.357, lines 22–29)*:
```
than executing the list operations in totality. Moreover, ndarray is strictly heterogeneous, unlike 
Python’s list collections.
But before we start our NumPy-FastAPI service implementation, we need to install the numpy module 
using the pip command:
pip install numpy
Our first API service will process some survey data and return it in ndarray form. The following 
get_respondent_answers() API retrieves a list of survey data from PostgreSQL through 
Piccolo and transforms the list of data into an ndarray:
```
[^203]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Comprehension** *(p.358)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.358, lines 27–34)*:
```
Data manipulation in an ndarray is easier and faster, unlike in a list collection, which requires list 
comprehension and loops. The vectors and matrices created by numpy have operations to manipulate 
their items, such as scalar multiplication, matrix multiplication, transposition, vectorization, and 
reshaping. The following API service shows how the product between a scalar gradient and an array 
of survey data is derived using the numpy module:
@router.get("/answer/increase/{gradient}")
async def answers_weight_multiply(gradient:int, qid:int):
    repo_loc = LocationRepository()
```
[^204]
**Annotation:** This excerpt demonstrates 'comprehension' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Constructor** *(p.337)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.337, lines 8–15)*:
```
Using the internal code base properties
FastAPI’s constructor has parameters that can replace the default info document details without using 
the get_openapi() function. The following snippet showcases a sample documentation update 
on the title, description, version, and servers details of the OpenAPI documentation:
app = FastAPI(… … … …, 
            title="The Online Restaurant Rating 
                       System API",
            description="This a software prototype.",
```
[^205]
**Annotation:** This excerpt demonstrates 'constructor' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.348)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.348, lines 23–25)*:
```
•	 Performing statistical analysis
•	 Generating CSV and XLSX reports
•	 Plotting data models
```
[^206]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 12: Deploying FastAPI Applications in the Cloud** *(pp.361–386)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, array.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^207]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 13: Converting APIs and Microservices** *(pp.387–404)*

This later chapter builds upon the concepts introduced here, particularly: None, as, async.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^208]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 14: Assessment Answers** *(pp.405–420)*

This later chapter builds upon the concepts introduced here, particularly: array, as, async.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^209]

**Annotation:** Forward reference: Chapter 14 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts array, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 12: Deploying FastAPI Applications in the Cloud

*Source: Building Python Microservices with FastAPI, pages 361–386*

### Chapter Summary
Details deploying FastAPI applications to cloud platforms. Covers Docker containerization, Kubernetes orchestration, deployment to AWS/Azure/GCP, Heroku, setting up CI/CD pipelines, managing production environments, scaling strategies, and infrastructure configuration. [^210]

### Concept-by-Concept Breakdown
#### **None** *(p.375)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.375, lines 7–14)*:
```
        
        if not result == None:
          ok = True
        else: 
          ok = False
        return CreateLoginData(loginData=result, ok=ok)
Similarly, the delete mutation class retrieves a record through an id and deletes it from the data store:
class DeleteLoginData(Mutation):
```
[^211]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.365)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.365, lines 6–13)*:
```
    df = pd.read_csv(StringIO(str(file.file.read(), 
               'utf-8')), encoding='utf-8')
    return templates.TemplateResponse('render_survey.html', 
         {'request': request, 'data': df.to_html()})
Aside from to_json() and to_html(), the TextFileReader object also has other converters 
that can help FastAPI render various content types, including to_latex(), to_excel(), 
to_hdf(), to_dict(), to_pickle(), and to_xarray(). Moreover, the pandas module 
has a read_excel() that can read XLSX content and convert it into any rendition type, just like 
```
[^212]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.374)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.374, lines 19–26)*:
```
CreateLoginData is a mutation that adds a new login record to the data store. The inner class, 
Arguments, indicates the record fields that will comprise the new login record for insertion. These 
arguments must appear in the overridden mutate() method to capture the values of these fields. 
This method will also call the ORM, which will persist the newly created record.
After a successful insert transaction, mutate() must return the class variables defined inside a 
mutation class such as ok and the loginData object. These returned values must be part of the 
mutation instance. 
Updating a login attribute has a similar implementation to CreateLoginData except the arguments 
```
[^213]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.365)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.365, lines 11–18)*:
```
that can help FastAPI render various content types, including to_latex(), to_excel(), 
to_hdf(), to_dict(), to_pickle(), and to_xarray(). Moreover, the pandas module 
has a read_excel() that can read XLSX content and convert it into any rendition type, just like 
its read_csv() counterpart.
Now, let us explore how FastAPI services can plot charts and graphs and output their graphical result 
through Response.
Plotting data models
With the help of the numpy and pandas modules, FastAPI services can generate and render different 
```
[^214]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.383)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.383, lines 4–11)*:
```
                 status_code=500)
The FastAPI framework can easily integrate into any database platform. The previous chapters have 
proven that FastAPI can deal with relational database transactions with ORM and document-based 
NoSQL transactions with ODM, while this chapter has proven the same for the Neo4j graph database 
due to its easy configurations.
Summary
This chapter introduced the scientific side of FastAPI by showing that API services can provide 
numerical computation, symbolic formulation, and graphical interpretation of data via the numpy, 
```
[^215]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 21 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.372)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.372, lines 14–21)*:
```
@router.post("/survey/save")
async def grouped_workflow(surveydata: SurveyDataResult):
    survey_dict = surveydata.dict(exclude_unset=True)
    result = group([save_result_xlsx
       .s(survey_dict['results']).set(queue='default'), 
         save_result_csv.s(len(survey_dict))
          .set(queue='default')]).apply_async()
    return {'message' : result.get(timeout = 10) } 
```
[^216]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.380)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.380, lines 3–10)*:
```
create_survey_loc() adds new survey location details to the Neo4j database. A record is 
considered a node in the graph database with a name and attributes equivalent to the record fields in 
the relational databases. We use the connection object to create a session that has a run() method 
to execute Cypher scripts.
The command to add a new node is CREATE, while the syntax to update, delete, and retrieve nodes 
can be added with the MATCH command. The following update_node_loc() service searches for 
a particular node based on the node’s name and performs the SET command to update the given fields:
@router.patch("/neo4j/update/location/{id}")
```
[^217]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.361)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.361, lines 5–12)*:
```
    repo_answers = AnswerRepository()
    locations = await repo_loc.get_all_location()
    data = []
    for loc in locations:
        loc_q = await repo_answers
           .get_answers_per_q(loc["id"], qid)
             if not len(loc_q) == 0:
                 loc_data = [ weights[qid-1]
```
[^218]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.374)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.374, lines 5–12)*:
```
      password = String(required=True)
    ok = Boolean()
    loginData = Field(lambda: LoginData)
    async def mutate(root, info, id, username, password):
        login_dict = {"id": id, "username": username, 
                   "password": password}
        login_json = dumps(login_dict, default=json_serial)
        repo = LoginRepository()
```
[^219]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.375)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.375, lines 12–19)*:
```
        return CreateLoginData(loginData=result, ok=ok)
Similarly, the delete mutation class retrieves a record through an id and deletes it from the data store:
class DeleteLoginData(Mutation):
    class Arguments:
      id = Int(required=True)
      
    ok = Boolean()
    loginData = Field(lambda: LoginData)
```
[^220]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.363)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.363, lines 32–36)*:
```
        row += 1
    workbook.close()
    output.seek(0)
    headers = {
        'Content-Disposition': 'attachment;
```
[^221]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Compiled** *(p.385)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.385, lines 13–20)*:
```
different and parallel installations of Python interpreters and their dependencies where each has the 
application(s) to be compiled and run. Each instance has its own set of libraries depending on the 
requirements of its application(s). But first, we need to install the virtualenv module to pursue 
the creation of these instances:
pip install virtualenv
The following list describes the benefits of having a virtual environment:
•	 To avoid the overlapping of the library version
•	 To avoid broken installed module files due to namespace collisions
```
[^222]
**Annotation:** This excerpt demonstrates 'compiled' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Constructor** *(p.362)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.362, lines 33–35)*:
```
object. From the given script, we store each data column in a separate list(), add all the lists in 
dict() with keys as column header names, and pass dict() as a parameter to the constructor 
of DataFrame.
```
[^223]
**Annotation:** This excerpt demonstrates 'constructor' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Coroutine** *(p.364)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.364, lines 23–30)*:
```
uploaded files because it supports more Pydantic features and has built-in operations that can work 
with coroutines. It can handle large file uploads without raising an change to - exception when the 
uploading process reaches the memory limit, unlike using the bytes type for file content storage. 
Thus, the given read-csv() service uses UploadFile to capture any CSV files for data analysis 
with orjson as its JSON serializer.
Another way to handle file upload transactions is through Jinja2 form templates. We can use 
TemplateResponse to pursue file uploading and render the file content using the Jinja2 templating 
language. The following service reads a CSV file using read_csv() and serializes it into HTML 
```
[^224]
**Annotation:** This excerpt demonstrates 'coroutine' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.364)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.364, lines 1–8)*:
```
Generating CSV and XLSX reports
341
             filename="list_respondents.xlsx"'
    }
    return StreamingResponse(output, headers=headers)
The given create_respondent_report_xlsx() service retrieves all the respondent records 
from the database and plots each profile record per row in the worksheet from the newly created 
Workbook. Instead of writing to a file, Workbook will store its content in a byte stream, io.ByteIO, 
```
[^225]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 12 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 13: Converting APIs and Microservices** *(pp.387–404)*

This later chapter builds upon the concepts introduced here, particularly: None, as, async.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^226]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 14: Assessment Answers** *(pp.405–420)*

This later chapter builds upon the concepts introduced here, particularly: array, as, async.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^227]

**Annotation:** Forward reference: Chapter 14 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts array, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 13: Converting APIs and Microservices

*Source: Building Python Microservices with FastAPI, pages 387–404*

### Chapter Summary
Covers converting existing APIs and microservices to FastAPI. Discusses migrating from Flask and Django, refactoring legacy applications, implementing API gateways, service integration patterns, modernization strategies, ensuring compatibility, and migration best practices. [^228]

### Concept-by-Concept Breakdown
#### **None** *(p.390)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.390, lines 5–12)*:
```
    # password=xxxx, # optional
    # max_tag_value_length=None # optional
)
span_processor = BatchSpanProcessor(jaeger_exporter)
tracer.add_span_processor(span_processor)
FastAPIInstrumentor.instrument_app(app, 
          tracer_provider=tracer)
LoggingInstrumentor().instrument(set_logging_format=True)
```
[^229]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.400)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.400, lines 1–8)*:
```
Integrating Flask and Django sub-applications
377
    }
} 
The application’s OpenAPI documentation can now be accessed through 
http://localhost:8080/docs.
The Dockerization of NGINX must come after deploying applications to the containers. But another 
approach is to include NGINX’s Dockerfile instructions in the application’s Dockerfile to 
```
[^230]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 30 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.393)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.393, lines 16–23)*:
```
@app.on_event(“startup”)
async def init():
    create_async_db() 
    global client
    client = EurekaClient(
     eureka_server=”http://DESKTOP-56HNGC9:8761/eureka”, 
     app_name=”sports_service”, instance_port=8000, 
     instance_host=”192.XXX.XXX.XXX”)
```
[^231]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.399)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.399, lines 10–17)*:
```
the IP address of the mongo container varies for every instance created. The following is the new 
AsyncIOMotorClient with the ch11-mongo service as the hostname:
def create_async_db():
    global client
    client = AsyncIOMotorClient(str(“ch11-mongo:27017”))
Now, let us implement an API Gateway design pattern for the containerized applications using the 
NGINX utility.
Using NGINX as an API Gateway
```
[^232]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.393)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.393, lines 23–28)*:
```
     instance_host=”192.XXX.XXX.XXX”)
    await client.start()
@app.on_event(“shutdown”)
async def destroy():
    close_async_db() 
    await client.stop()
```
[^233]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.403)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.403, lines 14–15)*:
```
we hope for more promising features in its future updates, such as support for reactive programming, 
circuit breakers, and a signature security module. We're hoping for the best for the FastAPI framework!
```
[^234]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.390)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.390, lines 13–20)*:
```
The first step in the preceding setup is to create a tracing service with a name using OpenTelemetry’s 
Resource class. Then, we instantiate a tracer from the service resource. To complete the setup, we need 
to provide the tracer with BatchSpanProcessor instantiated through the JaegerExporter 
details to manage all of the traces and logs using a Jaeger client. A trace includes full-detailed information 
about the exchange of requests and responses among all API services and other components across 
the distributed setup. This is unlike a log, which only contains the details regarding a transaction 
within an application.
After the completed Jaeger tracer setup, we integrate the tracer client with FastAPI through 
```
[^235]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.393)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.393, lines 26–28)*:
```
async def destroy():
    close_async_db() 
    await client.stop()
```
[^236]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.388)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.388, lines 23–25)*:
```
is preferred when managing API logs and traces. Tools such as Zipkin, Jaeger, and Skywalking are 
popular distributed tracing systems that can provide the setup for trace and log collections. In this 
prototype, we will be using the Jaeger tool to manage the application’s API traces and logs.
```
[^237]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.403)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.403, lines 12–15)*:
```
execution of API endpoints through its coroutines gives the framework the edge to become one of 
the most popular Python frameworks in the future. As the community of FastAPI continues to grow, 
we hope for more promising features in its future updates, such as support for reactive programming, 
circuit breakers, and a signature security module. We're hoping for the best for the FastAPI framework!
```
[^238]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Coroutine** *(p.403)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.403, lines 11–15)*:
```
framework, from creating background processes to rendering data using HTML templates. Its fast 
execution of API endpoints through its coroutines gives the framework the edge to become one of 
the most popular Python frameworks in the future. As the community of FastAPI continues to grow, 
we hope for more promising features in its future updates, such as support for reactive programming, 
circuit breakers, and a signature security module. We're hoping for the best for the FastAPI framework!
```
[^239]
**Annotation:** This excerpt demonstrates 'coroutine' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Custom Exception** *(p.404)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.404, lines 25–32)*:
```
about  30
custom exceptions  34-36
default handler override  37
HTTPException, raising  33, 34
multiple status codes  32, 33
single status code response  30-32
API responses
managing  39-41
```
[^240]
**Annotation:** This excerpt demonstrates 'custom exception' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.393)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.393, lines 16–23)*:
```
@app.on_event(“startup”)
async def init():
    create_async_db() 
    global client
    client = EurekaClient(
     eureka_server=”http://DESKTOP-56HNGC9:8761/eureka”, 
     app_name=”sports_service”, instance_port=8000, 
     instance_host=”192.XXX.XXX.XXX”)
```
[^241]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.404)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.404, lines 23–30)*:
```
checking  364, 365
API-related exceptions, managing
about  30
custom exceptions  34-36
default handler override  37
HTTPException, raising  33, 34
multiple status codes  32, 33
single status code response  30-32
```
[^242]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.404)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.404, lines 23–30)*:
```
checking  364, 365
API-related exceptions, managing
about  30
custom exceptions  34-36
default handler override  37
HTTPException, raising  33, 34
multiple status codes  32, 33
single status code response  30-32
```
[^243]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 14: Assessment Answers** *(pp.405–420)*

This later chapter builds upon the concepts introduced here, particularly: as, async, asyncio.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^244]

**Annotation:** Forward reference: Chapter 14 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, async appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 14: Assessment Answers

*Source: Building Python Microservices with FastAPI, pages 405–420*

### Chapter Summary
Provides assessment answers and solutions to chapter exercises. Includes detailed explanations for practice questions, reviews key concepts from each chapter, reinforces learning objectives, and serves as a reference guide for self-evaluation. [^245]

### Concept-by-Concept Breakdown
#### **Array** *(p.405)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.405, lines 6–13)*:
```
storing, in properties file  102-104
arrays
creating  334, 335
async/await construct
using  256, 257
async CRUD transactions, creating with Motor
about  182
asynchronous repository layer, 
```
[^246]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.405)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.405, lines 4–11)*:
```
managing  100
storing, as class attributes  101, 102
storing, in properties file  102-104
arrays
creating  334, 335
async/await construct
using  256, 257
async CRUD transactions, creating with Motor
```
[^247]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 36 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.405)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.405, lines 8–15)*:
```
creating  334, 335
async/await construct
using  256, 257
async CRUD transactions, creating with Motor
about  182
asynchronous repository layer, 
creating  183-185
CRUD transactions, running  185, 186
```
[^248]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 16 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.405)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.405, lines 20–27)*:
```
about  124
asyncio-compliant database 
drivers, installing  124
Base class, creating  125
CRUD transactions, running  129, 130
database connectivity, setting up  124, 125
model layer, creating  125
repository layer, building  126-128
```
[^249]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.405)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.405, lines 4–11)*:
```
managing  100
storing, as class attributes  101, 102
storing, in properties file  102-104
arrays
creating  334, 335
async/await construct
using  256, 257
async CRUD transactions, creating with Motor
```
[^250]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.405)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.405, lines 8–15)*:
```
creating  334, 335
async/await construct
using  256, 257
async CRUD transactions, creating with Motor
about  182
asynchronous repository layer, 
creating  183-185
CRUD transactions, running  185, 186
```
[^251]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.405)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.405, lines 4–11)*:
```
managing  100
storing, as class attributes  101, 102
storing, in properties file  102-104
arrays
creating  334, 335
async/await construct
using  256, 257
async CRUD transactions, creating with Motor
```
[^252]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Coroutine** *(p.406)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.406, lines 44–51)*:
```
managing  23, 24
coroutines
async/await construct, using  256, 257
asynchronous transactions, 
designing  258-260
@asyncio.coroutine, applying  255, 256
HTTP/2 protocol, using  261
implementing  254
```
[^253]
**Annotation:** This excerpt demonstrates 'coroutine' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.407)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.407, lines 25–32)*:
```
model layer, building  187, 188
CSV report
generating  338-342
cycle  29
D
database connectivity
preparing for  108, 109
database environment
```
[^254]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Dataframe** *(p.407)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.407, lines 33–40)*:
```
setting up  162-164
DataFrames
creating  334, 335
data models
about  62
plotting  342-346
decomposition pattern
applying  78, 79
```
[^255]
**Annotation:** This excerpt demonstrates 'dataframe' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.407)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.407, lines 5–12)*:
```
about  110, 116-118
Base class, defining  112
database connection, setting up  110, 111
database driver, installing  110
JOIN queries, creating  119, 120
model layer, building  112, 113
repository layer, implementing  116
session factory, initializing  111
```
[^256]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Dictionary** *(p.412)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.412, lines 70–72)*:
```
OAuth2 class, customizing  231, 232
permission dictionary, building  232, 233
scopes, applying to endpoints  234-236
```
[^257]
**Annotation:** This excerpt demonstrates 'dictionary' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.408)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.408, lines 21–28)*:
```
customizing  283
exception handlers
applying  84, 85
F
factory method pattern
about  100
using  100
FastAPI
```
[^258]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.408)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.408, lines 21–28)*:
```
customizing  283
exception handlers
applying  84, 85
F
factory method pattern
about  100
using  100
FastAPI
```
[^259]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.405)*

**Verbatim Educational Excerpt** *(FastAPI Microservices, p.405, lines 5–12)*:
```
storing, as class attributes  101, 102
storing, in properties file  102-104
arrays
creating  334, 335
async/await construct
using  256, 257
async CRUD transactions, creating with Motor
about  182
```
[^260]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---


---

### **Footnotes**

[^1]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 1, lines 1–25).
[^2]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 21, lines 17–24).
[^3]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 15, lines 7–14).
[^4]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 19, lines 2–9).
[^5]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 13, lines 25–32).
[^6]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 10, lines 84–91).
[^7]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 10, lines 44–51).
[^8]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 10, lines 43–50).
[^9]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 13, lines 17–24).
[^10]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 15, lines 18–25).
[^11]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 9, lines 8–15).
[^12]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 15, lines 8–15).
[^13]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 18, lines 15–22).
[^14]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 11, lines 30–37).
[^15]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 12, lines 80–87).
[^16]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 21, lines 19–26).
[^17]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 27, lines 1–1).
[^18]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 61, lines 1–1).
[^19]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 89, lines 1–1).
[^20]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 27, lines 1–25).
[^21]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 38, lines 16–23).
[^22]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 57, lines 17–24).
[^23]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 33, lines 15–22).
[^24]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 38, lines 5–12).
[^25]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 37, lines 1–8).
[^26]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 28, lines 5–12).
[^27]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 41, lines 2–9).
[^28]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 40, lines 19–26).
[^29]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 27, lines 7–14).
[^30]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 27, lines 7–14).
[^31]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 42, lines 27–34).
[^32]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 38, lines 7–14).
[^33]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 57, lines 7–14).
[^34]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 33, lines 12–19).
[^35]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 28, lines 18–25).
[^36]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 61, lines 1–1).
[^37]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 89, lines 1–1).
[^38]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 131, lines 1–1).
[^39]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 61, lines 1–25).
[^40]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 63, lines 33–36).
[^41]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 75, lines 11–18).
[^42]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 68, lines 22–29).
[^43]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 66, lines 1–8).
[^44]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 66, lines 1–8).
[^45]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 66, lines 4–11).
[^46]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 62, lines 7–14).
[^47]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 67, lines 6–13).
[^48]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 88, lines 8–15).
[^49]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 73, lines 5–12).
[^50]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 81, lines 10–17).
[^51]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 86, lines 4–11).
[^52]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 73, lines 7–14).
[^53]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 72, lines 11–18).
[^54]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 67, lines 24–31).
[^55]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 89, lines 1–1).
[^56]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 131, lines 1–1).
[^57]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 163, lines 1–1).
[^58]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 89, lines 1–25).
[^59]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 120, lines 2–9).
[^60]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 118, lines 12–19).
[^61]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 95, lines 10–17).
[^62]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 119, lines 8–15).
[^63]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 119, lines 15–22).
[^64]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 120, lines 15–22).
[^65]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 97, lines 24–31).
[^66]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 121, lines 3–10).
[^67]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 114, lines 6–13).
[^68]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 124, lines 6–13).
[^69]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 109, lines 26–33).
[^70]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 101, lines 20–27).
[^71]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 90, lines 4–11).
[^72]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 114, lines 31–32).
[^73]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 130, lines 3–10).
[^74]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 131, lines 1–1).
[^75]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 163, lines 1–1).
[^76]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 193, lines 1–1).
[^77]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 131, lines 1–25).
[^78]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 142, lines 4–11).
[^79]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 157, lines 9–16).
[^80]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 151, lines 32–34).
[^81]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 141, lines 4–11).
[^82]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 147, lines 1–8).
[^83]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 147, lines 2–9).
[^84]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 147, lines 4–11).
[^85]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 136, lines 3–10).
[^86]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 159, lines 2–9).
[^87]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 135, lines 22–29).
[^88]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 160, lines 9–16).
[^89]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 158, lines 26–33).
[^90]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 152, lines 7–14).
[^91]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 143, lines 20–27).
[^92]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 157, lines 25–32).
[^93]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 163, lines 1–1).
[^94]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 193, lines 1–1).
[^95]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 233, lines 1–1).
[^96]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 163, lines 1–25).
[^97]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 172, lines 12–19).
[^98]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 172, lines 17–24).
[^99]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 170, lines 31–35).
[^100]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 184, lines 2–9).
[^101]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 183, lines 16–23).
[^102]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 183, lines 17–24).
[^103]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 166, lines 10–17).
[^104]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 163, lines 8–15).
[^105]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 174, lines 2–9).
[^106]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 177, lines 2–9).
[^107]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 189, lines 3–10).
[^108]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 188, lines 22–29).
[^109]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 169, lines 30–37).
[^110]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 164, lines 9–16).
[^111]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 192, lines 4–11).
[^112]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 193, lines 1–1).
[^113]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 233, lines 1–1).
[^114]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 269, lines 1–1).
[^115]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 193, lines 1–25).
[^116]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 195, lines 2–9).
[^117]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 196, lines 15–22).
[^118]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 196, lines 16–23).
[^119]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 231, lines 10–17).
[^120]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 227, lines 17–24).
[^121]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 196, lines 3–10).
[^122]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 205, lines 17–24).
[^123]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 205, lines 19–26).
[^124]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 211, lines 21–28).
[^125]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 222, lines 2–9).
[^126]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 211, lines 23–30).
[^127]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 196, lines 15–22).
[^128]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 194, lines 2–9).
[^129]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 206, lines 7–14).
[^130]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 206, lines 2–9).
[^131]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 233, lines 1–1).
[^132]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 269, lines 1–1).
[^133]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 301, lines 1–1).
[^134]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 233, lines 1–25).
[^135]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 254, lines 3–10).
[^136]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 243, lines 24–31).
[^137]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 254, lines 30–36).
[^138]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 233, lines 4–11).
[^139]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 238, lines 1–8).
[^140]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 255, lines 10–17).
[^141]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 233, lines 23–30).
[^142]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 254, lines 24–31).
[^143]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 233, lines 2–9).
[^144]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 250, lines 16–22).
[^145]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 255, lines 16–23).
[^146]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 253, lines 9–16).
[^147]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 251, lines 26–33).
[^148]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 233, lines 6–13).
[^149]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 255, lines 19–26).
[^150]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 269, lines 1–1).
[^151]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 301, lines 1–1).
[^152]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 329, lines 1–1).
[^153]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 269, lines 1–25).
[^154]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 283, lines 6–13).
[^155]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 297, lines 3–10).
[^156]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 273, lines 29–36).
[^157]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 288, lines 11–18).
[^158]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 290, lines 7–14).
[^159]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 285, lines 27–34).
[^160]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 290, lines 1–8).
[^161]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 279, lines 2–9).
[^162]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 278, lines 2–9).
[^163]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 289, lines 7–14).
[^164]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 281, lines 13–20).
[^165]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 281, lines 19–26).
[^166]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 273, lines 12–19).
[^167]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 299, lines 12–19).
[^168]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 274, lines 13–20).
[^169]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 301, lines 1–1).
[^170]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 329, lines 1–1).
[^171]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 361, lines 1–1).
[^172]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 301, lines 1–25).
[^173]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 305, lines 22–29).
[^174]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 324, lines 4–11).
[^175]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 316, lines 15–22).
[^176]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 303, lines 7–14).
[^177]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 307, lines 4–11).
[^178]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 307, lines 7–14).
[^179]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 302, lines 3–10).
[^180]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 323, lines 5–12).
[^181]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 317, lines 6–13).
[^182]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 305, lines 8–15).
[^183]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 326, lines 10–17).
[^184]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 328, lines 7–14).
[^185]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 307, lines 5–12).
[^186]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 321, lines 7–14).
[^187]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 314, lines 13–20).
[^188]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 329, lines 1–1).
[^189]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 361, lines 1–1).
[^190]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 387, lines 1–1).
[^191]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 329, lines 1–25).
[^192]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 345, lines 8–15).
[^193]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 331, lines 8–15).
[^194]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 357, lines 15–22).
[^195]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 344, lines 2–9).
[^196]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 344, lines 17–24).
[^197]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 346, lines 11–18).
[^198]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 346, lines 11–18).
[^199]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 338, lines 8–15).
[^200]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 333, lines 4–11).
[^201]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 352, lines 14–21).
[^202]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 352, lines 10–17).
[^203]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 357, lines 22–29).
[^204]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 358, lines 27–34).
[^205]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 337, lines 8–15).
[^206]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 348, lines 23–25).
[^207]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 361, lines 1–1).
[^208]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 387, lines 1–1).
[^209]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 405, lines 1–1).
[^210]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 361, lines 1–25).
[^211]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 375, lines 7–14).
[^212]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 365, lines 6–13).
[^213]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 374, lines 19–26).
[^214]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 365, lines 11–18).
[^215]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 383, lines 4–11).
[^216]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 372, lines 14–21).
[^217]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 380, lines 3–10).
[^218]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 361, lines 5–12).
[^219]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 374, lines 5–12).
[^220]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 375, lines 12–19).
[^221]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 363, lines 32–36).
[^222]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 385, lines 13–20).
[^223]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 362, lines 33–35).
[^224]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 364, lines 23–30).
[^225]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 364, lines 1–8).
[^226]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 387, lines 1–1).
[^227]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 405, lines 1–1).
[^228]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 387, lines 1–25).
[^229]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 390, lines 5–12).
[^230]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 400, lines 1–8).
[^231]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 393, lines 16–23).
[^232]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 399, lines 10–17).
[^233]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 393, lines 23–28).
[^234]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 403, lines 14–15).
[^235]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 390, lines 13–20).
[^236]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 393, lines 26–28).
[^237]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 388, lines 23–25).
[^238]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 403, lines 12–15).
[^239]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 403, lines 11–15).
[^240]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 404, lines 25–32).
[^241]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 393, lines 16–23).
[^242]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 404, lines 23–30).
[^243]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 404, lines 23–30).
[^244]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 405, lines 1–1).
[^245]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 405, lines 1–25).
[^246]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 405, lines 6–13).
[^247]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 405, lines 4–11).
[^248]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 405, lines 8–15).
[^249]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 405, lines 20–27).
[^250]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 405, lines 4–11).
[^251]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 405, lines 8–15).
[^252]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 405, lines 4–11).
[^253]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 406, lines 44–51).
[^254]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 407, lines 25–32).
[^255]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 407, lines 33–40).
[^256]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 407, lines 5–12).
[^257]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 412, lines 70–72).
[^258]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 408, lines 21–28).
[^259]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 408, lines 21–28).
[^260]: Tragura, Sherwin John C.. *Building Python Microservices with FastAPI*. (JSON `Building Python Microservices with FastAPI.json`, p. 405, lines 5–12).
