# Comprehensive Python Guidelines — Python Microservices Development (Chapters 1-11)

*Source: Python Microservices Development, Chapters 1-11*

---

## Chapter 1: Understanding Microservices

*Source: Python Microservices Development, pages 8–31*

### Chapter Summary
Introduces microservices architecture, covering origins of Service-Oriented Architecture, comparing monolithic versus microservice approaches. Discusses microservice benefits including separation of concerns, smaller projects, and scaling. Explores potential pitfalls and implementing microservices with Python using WSGI, Greenlet, Gevent, Twisted, Tornado, and asyncio. [^1]

### Concept-by-Concept Breakdown
#### **Gil** *(p.22)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.22, lines 7–14)*:
```
ship new products and new features to their customers as fast as possible. They want to be
agile by iterating often, and they want to ship, ship, and ship again.
If thousands, or even millions, of customers use your service, pushing in production an
experimental feature, and removing it if it does not work, is considered good practice rather
than baking it for months before you publish it.
Companies such as Netflix are promoting their continuous delivery techniques where small
changes are made very often into production, and tested on a subset of the user base.
They've developed tools such as Spinnaker (h t t p ://w w w . s p i n n a k e r . i o /) to automate as
```
[^2]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.26)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.26, lines 2–9)*:
```
[ 12 ]
The deployment is also a no brainer: we can tag the code base, build a package, and run it
somewhere. To scale it, we can run several instances of the booking app, and run several
databases with some replication mechanism in place.
If your application stays small, this model works well and is easy to maintain for a single
team.
But projects are usually growing, and they get bigger than what was first intended. And
having the whole application in a single code base brings some nasty issues along the way.
```
[^3]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 16 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.13)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.13, lines 13–20)*:
```
194
Asserting incoming data
194
Limiting your application scope
198
Using Bandit linter
199
Summary
```
[^4]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.12)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.12, lines 19–26)*:
```
137
Asynchronous calls
137
Task queues
138
Topic queues
139
Publish/subscribe
```
[^5]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.10)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.10, lines 39–46)*:
```
25
asyncio
26
Language performances
29
Summary
31
Chapter 2: Discovering Flask
```
[^6]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.27)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.27, lines 2–9)*:
```
[ 13 ]
Any change in the code can impact unrelated features. When something breaks,
the whole application may break.
Solutions to scale your application are limited: you can deploy several instances,
but if one particular feature inside the app takes all the resources, it impacts
everything.
As the code base grows, it's hard to keep it clean and under control.
There are, of course, some ways to avoid some of the issues described here.
```
[^7]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.30)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.30, lines 20–27)*:
```
level, a philosophy similar to the single responsibility principle.
The single responsibility principle was defined by Robert Martin to explain that a class
should have only one reason to change; in other words, each class should provide a single,
well-defined feature. Applied to microservices, it means that we want to make sure that
each microservice focuses on a single role.
Smaller projects
The second benefit is breaking the complexity of the project. When you add a feature to an
application such as PDF reporting, even if you do it cleanly, you make the base code bigger,
```
[^8]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.21)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.21, lines 18–20)*:
```
Runnerly, which is available on GitHub for you to study. You can interact with me there,
point mistakes if you see any, and we can continue to learn about writing excellent Python
apps together.
```
[^9]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Coroutine** *(p.14)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.14, lines 51–58)*:
```
298
Coroutines
301
The asyncio library
303
The aiohttp framework
304
Sanic
```
[^10]
**Annotation:** This excerpt demonstrates 'coroutine' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Debugging** *(p.11)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.11, lines 9–16)*:
```
56
Error handling and debugging
57
Custom error handler
58
The debug mode
60
A microservice skeleton
```
[^11]
**Annotation:** This excerpt demonstrates 'debugging' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.29)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.29, lines 28–35)*:
```
In that context, microservices are logical units that focus on a very particular task. Here's a
full definition attempt:
A microservice is a lightweight application, which provides a narrowed
list of features with a well-defined contract. It's a component with a single
responsibility, which can be developed and deployed independently.
This definition does not mention HTTP or JSON, because you could consider a small UDP-
based service that exchanges binary data as a microservice for example.
But in our case, and throughout the book, all our microservices are just simple web
```
[^12]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.18)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.18, lines 15–22)*:
```
You can download the example code files for this book from your account at h t t p ://w w w . p
a c k t p u b . c o m . If you purchased this book elsewhere, you can visit h t t p ://w w w . p a c k t p u b . c
o m /s u p p o r t and register to have the files e-mailed directly to you.
You can download the code files by following these steps:
Log in or register to our website using your e-mail address and password.
1.
Hover the mouse pointer on the SUPPORT tab at the top.
2.
```
[^13]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Error Handling** *(p.11)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.11, lines 9–16)*:
```
56
Error handling and debugging
57
Custom error handler
58
The debug mode
60
A microservice skeleton
```
[^14]
**Annotation:** This excerpt demonstrates 'error handling' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.18)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.18, lines 14–21)*:
```
Downloading the example code
You can download the example code files for this book from your account at h t t p ://w w w . p
a c k t p u b . c o m . If you purchased this book elsewhere, you can visit h t t p ://w w w . p a c k t p u b . c
o m /s u p p o r t and register to have the files e-mailed directly to you.
You can download the code files by following these steps:
Log in or register to our website using your e-mail address and password.
1.
Hover the mouse pointer on the SUPPORT tab at the top.
```
[^15]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.31)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.31, lines 12–19)*:
```
Scaling and deployment
Finally, having your application split into components makes it easier to scale depending on
your constraints. Let's say you start getting a lot of customers who book hotels daily, and
the PDF generation starts to heat up the CPUs. You can deploy that specific microservice in
some servers that have bigger CPUs.
Another typical example are RAM-consuming microservices like the ones that interact with
memory databases like Redis or Memcache. You could tweak your deployments,
consequently, by deploying them on servers with less CPU and a lot more RAM.
```
[^16]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 2: Discovering Flask** *(pp.33–64)*

This later chapter builds upon the concepts introduced here, particularly: GIL, as, assert.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^17]

**Annotation:** Forward reference: Chapter 2 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 3: Coding, Testing, and Documenting - the Virtuous Cycle** *(pp.65–94)*

This later chapter builds upon the concepts introduced here, particularly: GIL, as, assert.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^18]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Designing Runnerly** *(pp.95–120)*

This later chapter builds upon the concepts introduced here, particularly: as, break, class.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^19]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 2: Discovering Flask

*Source: Python Microservices Development, pages 33–64*

### Chapter Summary
Explores Flask framework for building microservices in Python. Covers Flask basics, routing, request handling, extensions and middlewares, templates, configuration, and blueprints. Details error handling, debugging modes, and creating a microservice skeleton with Flask. [^20]

### Concept-by-Concept Breakdown
#### **Gil** *(p.43)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.43, lines 21–28)*:
```
One controversial topic in the Python community around speeding up the language is how
the Global Interpreter Lock (GIL) mutex can ruin performances, because multi-threaded
applications cannot use several processes.
The GIL has good reasons to exist. It protects non-thread-safe parts of the CPython
interpreter, and exists in other languages like Ruby. And all attempts to remove it so far
have failed to produce a faster CPython implementation.
Larry Hasting is working on a GIL-free CPython project called Gilectomy
(h t t p s ://g i t h u b . c o m /l a r r y h a s t i n g s /g i l e c t o m y ). Its minimal goal is to
```
[^21]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.60)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.60, lines 20–27)*:
```
    app = Flask(__name__)
    def yamlify(data, status=200, headers=None):
        _headers = {'Content-Type': 'application/x-yaml'}
        if headers is not None:
            _headers.update(headers)
        return yaml.safe_dump(data), status, _headers
    @app.route('/api')
    def my_microservice():
```
[^22]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.52)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.52, lines 33–37)*:
```
 'wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w'
     encoding='UTF-8'>, 'CONTENT_TYPE': ''}
 <Response 24 bytes [200 OK]>
 b'{n  "Hello": "World!"n}n'
 127.0.0.1 - - [22/Dec/2016 15:07:01] "GET /api HTTP/1.1" 200
```
[^23]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.50)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.50, lines 16–23)*:
```
        return jsonify({'Hello': 'World!'})
    if __name__ == '__main__':
        app.run()
That app returns a JSON mapping when called on /api. Every other endpoint would
return a 404 Error.
The __name__ variable, whose value will be __main__ when you run that single Python
module, is the name of the application package. It's used by Flask to instantiate a new
logger with that name, and to find where the file is located on the disk. Flask will use the
```
[^24]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.50)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.50, lines 12–19)*:
```
    from flask import Flask, jsonify
    app = Flask(__name__)
    @app.route('/api')
    def my_microservice():
        return jsonify({'Hello': 'World!'})
    if __name__ == '__main__':
        app.run()
That app returns a JSON mapping when called on /api. Every other endpoint would
```
[^25]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.55)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.55, lines 5–12)*:
```
implementation description taken from Werkzeug's routing module:
Rules without any arguments come first for performance. This is
1.
because we expect them to match faster and some common
rules usually don't have any arguments (index pages, and so
on).
The more complex rules come first, so the second argument is
2.
```
[^26]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.60)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.60, lines 5–12)*:
```
str: The data gets encoded as UTF-8 and used as the HTTP response body.
bytes/bytesarray: Used as the body.
A (response, status, headers) tuple: Where response can be a Response object or
one of the previous types. status is an integer value that overwrites the response
status, and headers is a mapping that extends the response headers.
A (response, status) tuple: Like the previous one, but without specific headers
A (response, headers) tuple: Like the preceding one, but with just extra headers.
Any other case will lead to an exception.
```
[^27]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.42)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.42, lines 2–9)*:
```
[ 28 ]
And that's what's going to be used at every level of an async Python app going forward.
Here's another example using aiopg, a PostgreSQL library for asyncio from the project
documentation:
    import asyncio
    import aiopg
    dsn = 'dbname=aiopg user=aiopg password=passwd host=127.0.0.1'
    async def go():
```
[^28]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 23 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.42)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.42, lines 16–23)*:
```
                    ret.append(row)
                assert ret == [(1,)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())
With a few async and await prefixes, the function that performs an SQL query and sends
back the result looks a lot like a synchronous function.
But asynchronous frameworks and libraries based on Python 3 are still emerging, and if you
are using asyncio or a framework like aiohttp, you will need to stick with particular
```
[^29]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.42)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.42, lines 2–9)*:
```
[ 28 ]
And that's what's going to be used at every level of an async Python app going forward.
Here's another example using aiopg, a PostgreSQL library for asyncio from the project
documentation:
    import asyncio
    import aiopg
    dsn = 'dbname=aiopg user=aiopg password=passwd host=127.0.0.1'
    async def go():
```
[^30]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 16 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.42)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.42, lines 3–10)*:
```
And that's what's going to be used at every level of an async Python app going forward.
Here's another example using aiopg, a PostgreSQL library for asyncio from the project
documentation:
    import asyncio
    import aiopg
    dsn = 'dbname=aiopg user=aiopg password=passwd host=127.0.0.1'
    async def go():
        pool = await aiopg.create_pool(dsn)
```
[^31]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.58)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.58, lines 18–25)*:
```
The bottom line is that a view can introspect the incoming request through the request
object attributes without having to deal with some parsing. The work done by Flask is quite
high level. For instance, the Authorization header is looked at and decomposed
automatically when possible.
In the following example, an HTTP Basic Auth that is sent by the client is always
converted to a base64 form when sent to the server. Flask will detect the Basic prefix, and
will parse it into username and password fields in the request.authorization
attribute:
```
[^32]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.42)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.42, lines 9–16)*:
```
    async def go():
        pool = await aiopg.create_pool(dsn)
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1")
                ret = []
                async for row in cur:
                    ret.append(row)
```
[^33]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.53)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.53, lines 3–10)*:
```
Let's explore what's happening here on the call:
Routing: Flask creates the Map class
Request: Flask passes a Request object to the view
Response: A Response object is sent back with the response content
Routing
The routing happens in app.url_map, which is an instance of Werkzeug's Map class. That
class uses regular expressions to determine if a function decorated by @app.route matches
the incoming request. The routing only looks at the path you provided in the route call to
```
[^34]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.41)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.41, lines 6–13)*:
```
implement coroutines, made asynchronous applications built with vanilla Python 3.5+ code
look very elegant and close to synchronous programming.
Coroutines are functions that can suspend and resume their execution.
Chapter 12, What Next?, explains in detail how they are implemented in
Python and how to use them.
By doing this, Python did a great job at avoiding the callback syntax mess we sometimes see
in Node.js or Twisted (Python 2) applications.
And beyond coroutines, Python 3 has introduced a full set of features and helpers in the
```
[^35]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 3: Coding, Testing, and Documenting - the Virtuous Cycle** *(pp.65–94)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^36]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Designing Runnerly** *(pp.95–120)*

This later chapter builds upon the concepts introduced here, particularly: None, __main__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^37]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __main__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Interacting with Other Services** *(pp.121–150)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^38]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 3: Coding, Testing, and Documenting - the Virtuous Cycle

*Source: Python Microservices Development, pages 65–94*

### Chapter Summary
Covers the development cycle of coding, testing, and documenting microservices. Details different test types including unit, functional, integration, load, and end-to-end tests. Introduces WebTest, pytest, and Tox for testing. Discusses developer documentation practices and continuous integration with Travis-CI, ReadTheDocs, and Coveralls. [^39]

### Concept-by-Concept Breakdown
#### **Gil** *(p.79)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.79, lines 8–11)*:
```
code you are creating, will not always improve the quality of your project, but it will make
your team more agile. This means that the developers who need to fix a bug, or refactor a
part of an application, will be able to do a faster and better job when relying on a battery of
tests. If they break a feature, the tests should warn them about it.
```
[^40]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.69)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.69, lines 2–9)*:
```
[ 55 ]
         'SESSION_COOKIE_DOMAIN': None, 'SECRET_KEY': None,
         'EXPLAIN_TEMPLATE_LOADING': False,
         'TRAP_BAD_REQUEST_ERRORS': False,
         'SESSION_REFRESH_EACH_REQUEST': True,
         'TEMPLATES_AUTO_RELOAD': None,
         'JSONIFY_PRETTYPRINT_REGULAR': True,
         'SESSION_COOKIE_PATH': None,
```
[^41]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.76)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.76, lines 22–29)*:
```
myservices/: The actual package
__init__.py
app.py: The app module, which contains the app itself
views/: A directory containing the views organized in blueprints
__init__.py
home.py: The home blueprint, which serves the root
endpoint
tests: The directory containing all the tests
```
[^42]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.66)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.66, lines 3–10)*:
```
        return jsonify({'Hello': ip})
    if __name__ == '__main__':
        app.run()
Notice that we use app.wsgi_app here to wrap the WSGI app. In Flask,
the app object is not the WSGI application itself as we've seen earlier.
Tampering with the WSGI environ before your application gets it is fine, but if you want
to implement anything that will impact the response, doing it inside a WSGI middleware is
going to make your work very painful.
```
[^43]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.72)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.72, lines 26–33)*:
```
    from flask import Flask, jsonify
    app = Flask(__name__)
    @app.errorhandler(500)
    def error_handling(error):
        return jsonify({'Error': str(error)}, 500)
    @app.route('/api')
    def my_microservice():
        raise TypeError("Some Exception")
```
[^44]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.82)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.82, lines 10–17)*:
```
Testing in isolation in Python usually means that you instantiate a class or call a function
with specific arguments, and verify that you get the expected result. When the class or
function calls another piece of code that's not built in Python or its standard library, it's not
in isolation anymore.
In some cases, it will be useful to mock those calls to achieve isolation. Mocking means 
replacing a piece of code with a mock version, which takes specified input, yields specified
outputs, and fakes the behavior in between. But mocking is often a dangerous exercise,
because it's easy to implement a different behavior in your mocks and end up with some
```
[^45]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.93)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.93, lines 3–10)*:
```
Using WebTest
WebTest (h t t p ://w e b t e s t . r e a d t h e d o c s . i o ) has been around for a long time. It was 
written by Ian Bicking back in the days of the Paste project, and is based on the WebOb (h t
t p ://d o c s . w e b o b . o r g ) project, which provides a Request and Response class similar (but
not compatible) to Flask's.
WebTest wraps call to a WSGI application like FlaskTest does, and lets you interact with
it. WebTest is somewhat similar to FlaskTest, with a few extra helpers when dealing with
JSON, and a neat feature to call non-WSGI applications.
```
[^46]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 23 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.86)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.86, lines 5–12)*:
```
            hello = app.get('/api')
            # asserting the body
            body = json.loads(str(hello.data, 'utf8'))
            self.assertEqual(body['Hello'], 'World!')
    if __name__ == '__main__':
        unittest.main()
The FlaskClient class has one method per HTTP verb, and sends back Response objects
that can be used to assert the results. In the preceding example, we used .get().
```
[^47]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.90)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.90, lines 10–17)*:
```
    @scenario(5)
    async def scenario_one(session):
        res = await session.get('http://localhost:5000/api').json()
        assert res['Hello'] == 'World!'
    @scenario(30)
    async def scenario_two(session):
        somedata = json.dumps({'OK': 1})
        res = await session.post('http://localhost:5000/api',
```
[^48]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.65)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.65, lines 16–23)*:
```
environment when you want to make sure your application behaves properly when it tries
to get the remote IP address, since the remote_addr attribute will get the IP of the proxy,
not the real client:
    from flask import Flask, jsonify, request
    import json
    class XFFMiddleware(object):
        def __init__(self, app, real_ip='10.1.1.1'):
            self.app = app
```
[^49]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.90)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.90, lines 11–18)*:
```
    async def scenario_one(session):
        res = await session.get('http://localhost:5000/api').json()
        assert res['Hello'] == 'World!'
    @scenario(30)
    async def scenario_two(session):
        somedata = json.dumps({'OK': 1})
        res = await session.post('http://localhost:5000/api',
                                 data=somedata)
```
[^50]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.69)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.69, lines 39–40)*:
```
top of ConfigParser, which automates the conversion of simple types like integers and
Booleans.
```
[^51]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.79)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.79, lines 10–11)*:
```
part of an application, will be able to do a faster and better job when relying on a battery of
tests. If they break a feature, the tests should warn them about it.
```
[^52]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.82)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.82, lines 5–12)*:
```
everything needed to write some. In a project based on Flask, there usually are, alongside
the views, some functions and classes, which can be unit-tested in isolation.
However, the concept of separation is quite vague for a Python project, because we don't use
contracts or interfaces like in other languages, where the implementation of the class is
separated from its definition.
Testing in isolation in Python usually means that you instantiate a class or call a function
with specific arguments, and verify that you get the expected result. When the class or
function calls another piece of code that's not built in Python or its standard library, it's not
```
[^53]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Datetime** *(p.67)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.67, lines 27–34)*:
```
RFC 822 message, which you can send via SMTP:
    from datetime import datetime
    from jinja2 import Template
    from email.utils import format_datetime
    def render_email(**data):
        with open('email_template.eml') as f:
            template = Template(f.read())
        return template.render(**data)
```
[^54]
**Annotation:** This excerpt demonstrates 'datetime' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 4: Designing Runnerly** *(pp.95–120)*

This later chapter builds upon the concepts introduced here, particularly: None, __main__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^55]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __main__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Interacting with Other Services** *(pp.121–150)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^56]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Monitoring Your Services** *(pp.151–180)*

This later chapter builds upon the concepts introduced here, particularly: None, __main__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^57]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __main__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 4: Designing Runnerly

*Source: Python Microservices Development, pages 95–120*

### Chapter Summary
Presents the design of Runnerly, a practical microservices application example. Covers user stories, application architecture, service decomposition, and design patterns for microservices. Demonstrates real-world application of microservice principles. [^58]

### Concept-by-Concept Breakdown
#### **None** *(p.118)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.118, lines 3–10)*:
```
    celery = Celery(__name__, backend=BACKEND, broker=BROKER)
_APP = None
    def activity2run(user, activity):
        “”””Used by fetch_runs to convert a strava run into a DB entry.
        ”””
        run = Run()
        run.runner = user
        run.strava_id = activity.id
```
[^59]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Pep 8** *(p.102)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.102, lines 16–23)*:
```
Tox can automate every step you are doing when you change something in your project:
running tests on various Python interpreters, verifying coverage and PEP 8 conformance,
building documentation, and so on.
But running all the checks on every change can be time and resource consuming, in
particular, if you support several interpreters.
A Continuous Integration (CI) system solves this issue by taking care of this work every
time something changes in your project.
Pushing your project in a shared repository under a Distributed Version Control System
```
[^60]
**Annotation:** This excerpt demonstrates 'PEP 8' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.99)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.99, lines 14–21)*:
```
        return "Hello World!"
    if __name__ == "__main__":
        app.run()
That snippet is a fully working app!
But adding code snippets in your documentation means that they might get deprecated as
soon as you change your code. To avoid deprecation, one method is to have every code
snippet displayed in your documentation extracted from the code itself.
To do this, you can document your modules, classes, and functions with their docstrings,
```
[^61]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.99)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.99, lines 10–17)*:
```
    from flask import Flask
    app = Flask(__name__)
    @app.route("/")
    def hello():
        return "Hello World!"
    if __name__ == "__main__":
        app.run()
That snippet is a fully working app!
```
[^62]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.117)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.117, lines 23–30)*:
```
(http://www.rabbitmq.com), and Amazon SQS (https://aws.amazon.com/sqs/) and
provides an abstraction for a Python app to work on both sides of it: to send and run jobs.
The part that runs the job is called a worker, and Celery provides a Celery class to start
one. To use celery from a Flask application, you can create a background.py module that
instantiates a Celery object and marks your background tasks with a @celery.task
decorator.
In the following example, we're using the stravalib (http://pythonhosted.org/stravalib)
library to grab runs from Strava for each user in Runnerly that has a Strava token:
```
[^63]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.113)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.113, lines 2–9)*:
```
[ 99 ]
Using the Flask-SQLAlchemy (http://flask-sqlalchemy.pocoo.org/) extension, you can 
specify the tables using the Model class as a base class. The following is the definition for
the User table with the SQLAlchemy class:
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()
    class User(db.Model):
        __tablename__ = 'user'
```
[^64]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 20 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.115)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.115, lines 8–15)*:
```
                   'age', 'weight', 'max_hr', 'rest_hr', 'vo2max']
The display attribute is just a helper to help the template iterate into a particular ordered list
of fields when rendering the form. Everything else is using WTForms basic fields classes to
create a form for the user table. The WTForm's Fields documentation provides the full list at
http://wtforms.readthedocs.io/en/latest/fields.html.
Once created, UserForm can be used in a view that has two goals. The first one is to display
the form on GET calls, and the second one is to update the database on POST calls when the
user submits the form:
```
[^65]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.103)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.103, lines 19–26)*:
```
That matrix can be matched with your Tox environments by running each one of them
separately via tox -e. By doing this, you will be able to know when a change breaks a
particular environment:
language: python
python: 3.5
env:
 - TOX_ENV=py27
 - TOX_ENV=py35
```
[^66]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.113)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.113, lines 3–10)*:
```
Using the Flask-SQLAlchemy (http://flask-sqlalchemy.pocoo.org/) extension, you can 
specify the tables using the Model class as a base class. The following is the definition for
the User table with the SQLAlchemy class:
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()
    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
```
[^67]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.118)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.118, lines 33–40)*:
```
                if user.strava_token is None:
                    continue
                runs_fetched[user.id] = fetch_runs(user)
        return runs_fetched
    def fetch_runs(user):
        client = Client(access_token=user.strava_token)
        runs = 0
        for activity in client.get_activities(limit=10):
```
[^68]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Decorator** *(p.117)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.117, lines 27–34)*:
```
instantiates a Celery object and marks your background tasks with a @celery.task
decorator.
In the following example, we're using the stravalib (http://pythonhosted.org/stravalib)
library to grab runs from Strava for each user in Runnerly that has a Strava token:
    from celery import Celery
    from stravalib import Client
    from monolith.database import db, User, Run
    BACKEND = BROKER = 'redis://localhost:6379'
```
[^69]
**Annotation:** This excerpt demonstrates 'decorator' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.118)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.118, lines 4–11)*:
```
_APP = None
    def activity2run(user, activity):
        “”””Used by fetch_runs to convert a strava run into a DB entry.
        ”””
        run = Run()
        run.runner = user
        run.strava_id = activity.id
        run.name = activity.name
```
[^70]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Docstring** *(p.99)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.99, lines 20–27)*:
```
snippet displayed in your documentation extracted from the code itself.
To do this, you can document your modules, classes, and functions with their docstrings,
and use the Autodoc Sphinx extension (h t t p ://w w w . s p h i n x - d o c . o r g /e n /l a t e s t /e x t /a u t
o d o c . h t m l ), which grabs docstrings to inject them in the documentation.
This is how Python documents its standard library at h t t p s ://d o c s . p y t h o n . o r g /3/l i b r a r
y /i n d e x . h t m l . In the following example, the autofunction directive will catch the
docstring from the index function that's located in the myservice/views/home.py
module:
```
[^71]
**Annotation:** This excerpt demonstrates 'docstring' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.106)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.106, lines 3–10)*:
```
For Coveralls to work from Travis, there are a few environment variables that need to be
passed via passenv; everything else should work automatically.
Every time you change your project and Travis-CI triggers a build, it will, in turn, trigger
Coveralls to display an excellent summary of the coverage and how it evolves over time,
like in the preceding screenshot.
Many other services can be hooked on GitHub or Travis-CI, Coveralls being one example.
Once you start to add services to your project, it's good practice to use badges in your
project's README so the community can see in one glance the status for each one of them
```
[^72]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.96)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.96, lines 10–17)*:
```
definition, found 1
test_app.py:21:1: W391 blank line at end of file
______________ FLAKE8-check ___________________________________
test_app_webtest.py:29:1: W391 blank line at end of file
______________ FLAKE8-check ___________________________________
test_bugzilla.py:26:80: E501 line too long (80 > 79 characters)
test_bugzilla.py:28:80: E501 line too long (82 > 79 characters)
test_bugzilla.py:40:1: W391 blank line at end of file
```
[^73]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 5: Interacting with Other Services** *(pp.121–150)*

This later chapter builds upon the concepts introduced here, particularly: None, __main__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^74]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __main__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Monitoring Your Services** *(pp.151–180)*

This later chapter builds upon the concepts introduced here, particularly: None, __main__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^75]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __main__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Securing Your Services** *(pp.181–202)*

This later chapter builds upon the concepts introduced here, particularly: None, __name__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^76]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __name__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 5: Interacting with Other Services

*Source: Python Microservices Development, pages 121–150*

### Chapter Summary
Details inter-service communication patterns including synchronous and asynchronous calls. Covers HTTP sessions, connection pooling, cache headers, data transfer optimization with GZIP compression and binary payloads. Introduces task queues, topic queues, publish/subscribe patterns, RPC over AMQP, and testing strategies for mocking service calls. [^77]

### Concept-by-Concept Breakdown
#### **Gil** *(p.127)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.127, lines 4–11)*:
```
Flask application in the first place?" That design was excellent when we started to code
Runnerly, but it became obvious that it's fragile.
The interactions Celery has with the application are very specific. The Strava worker needs
to:
Get the Strava tokens
Add new runs
Instead of using the Flask app code, the Celery worker code could be entirely independent
and just interacts with the database directly.
```
[^78]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.144)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.144, lines 7–14)*:
```
The get_user() method returns a user entry from _USERS and sets the ETag value with
response.set_etag. When the view gets some calls, it also looks for the If-None-Match
header to compare it to the user's modified field, and returns a 304 response if it matches:
    import time
    from flask import Flask, jsonify, request, Response, abort
    app = Flask(__name__)
    def _time2etag(stamp=None):
        if stamp is None:
```
[^79]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.122)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.122, lines 19–26)*:
```
        # ... all the Columns ...
        def __init__(self, *args, **kw):
            super(User, self).__init__(*args, **kw)
            self._authenticated = False
        def set_password(self, password):
            self.password = generate_password_hash(password)
        @property
        def is_authenticated(self):
```
[^80]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.138)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.138, lines 22–29)*:
```
        return jsonify({'result': sub_result, 'Hello': 'World!'})
    if __name__ == '__main__':
        app.run(port=5001)
A call to the service will propagate a call to the other service:
$ curl http://127.0.0.1:5001/api
{
  "Hello": "World!",
  "result": {
```
[^81]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.138)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.138, lines 15–22)*:
```
    from flask import Flask, jsonify
    app = Flask(__name__)
    setup_connector(app)
    @app.route('/api', methods=['GET', 'POST'])
    def my_microservice():
        with get_connector(app) as conn:
            sub_result = conn.get('http://localhost:5000/api').json()
        return jsonify({'result': sub_result, 'Hello': 'World!'})
```
[^82]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.125)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.125, lines 11–18)*:
```
It's a short and clean implementation on the top of a relational database that can be
deployed with a PostgreSQL or MySQLServer. Thanks to the SQLAlchemy abstractions, a
local version can run with SQLite 3 and facilitate your day-to-day work and your tests.
To build this app, we've used the following extensions and library:
Flask-SQLAlchemy and SQLAlchemy: These are used for the Model
Flask-WTF and WTForms: These are used for all the forms
Celery and Redis: These are used for background processes and periodic tasks
Flask-Login: This is used for managing authentication and authorization
```
[^83]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.122)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.122, lines 19–26)*:
```
        # ... all the Columns ...
        def __init__(self, *args, **kw):
            super(User, self).__init__(*args, **kw)
            self._authenticated = False
        def set_password(self, password):
            self.password = generate_password_hash(password)
        @property
        def is_authenticated(self):
```
[^84]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.130)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.130, lines 6–13)*:
```
            schema:
                type: array
                items:
                    type: integer
The full Open API 2.0 specification can be found at http://swagger.io/specification/.
It's very detailed and will let you describe metadata about the API, its endpoints, and the
data types it uses.
The data types described in the schema sections are following the JSON-Schema
```
[^85]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.122)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.122, lines 5–12)*:
```
matters the most. When the authentication process happens, there's a
window during which an attacker can intercept the password (in clear or
hashed form). In Chapter 7, Securing Your Services, we'll talk about ways
to reduce this attack surface.
Werkzeug provides a few helpers to deal with password hashes,
generate_password_hash() and check_password_hash(), which can be integrated
into our User class.
By default, Werkzeug uses PBKDF2 (https://en.wikipedia.org/wiki/PBKDF2) with
```
[^86]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 34 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.135)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.135, lines 8–15)*:
```
On the other hand, the Celery workers are doing their duty in the background, and they
receive their order via a Redis broker asynchronously.
There are also cases where a mix of synchronous and asynchronous calls are useful. For
instance, letting the user pick a new training plan can trigger the creation of a series of new
runs in the background while displaying some info about the plan itself.
In future versions of Runnerly, we could also have more service-to-service interactions,
where an event in a service triggers a series of reactions in other services. Having the ability
to loosely couple different parts of the system via some asynchronous messaging is quite
```
[^87]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.124)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.124, lines 24–31)*:
```
change their info.
If we add an is_admin Boolean flag in the User model, we can create a similar decorator
such as @login_required, which will also check this flag:
    def admin_required(func):
        @functools.wraps(func)
        def _admin_required(*args, **kw):
            admin = current_user.is_authenticated and current_user.is_admin
            if not admin:
```
[^88]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.122)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.122, lines 10–17)*:
```
generate_password_hash() and check_password_hash(), which can be integrated
into our User class.
By default, Werkzeug uses PBKDF2 (https://en.wikipedia.org/wiki/PBKDF2) with
SHA-1, which is a secure way to hash a value with salt.
Let's extend our User class with methods to set and verify a password:
    from werkzeug.security import generate_password_hash,
check_password_hash
    class User(db.Model):
```
[^89]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Constructor** *(p.141)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.141, lines 28–31)*:
```
inherits from HTTPAdapter, which surfaces urllib3 pool options.
You can pass these options to the constructor:
pool_connections: This helps you figure out how many simultaneous
connections are kept open.
```
[^90]
**Annotation:** This excerpt demonstrates 'constructor' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Datetime** *(p.150)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.150, lines 30–37)*:
```
{1: 2}
But there's also the problem of date representations: DateTime objects are not directly
serializable in JSON and MessagePack, so you need to make sure you convert them.
In any case, in a world of microservices where JSON is the most accepted standard, sticking
with string keys and taking care of dates are minor annoyances to stick with a universally
adopted standard.
Unless all your services are in Python with well-defined structures, and
you need to speed up the serialization steps as much as possible, it's
```
[^91]
**Annotation:** This excerpt demonstrates 'datetime' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Decorator** *(p.124)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.124, lines 8–15)*:
```
the user edition form should not be accessible if you are not logged in. The
@login_required decorator will reject any attempt to access a view if you are not logged
in with a 401 Unauthorized error.
It needs to be placed after the @app.route() call:
    @app.route('/create_user', methods=['GET', 'POST'])
    @login_required
    def create_user():
        # ... code
```
[^92]
**Annotation:** This excerpt demonstrates 'decorator' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 6: Monitoring Your Services** *(pp.151–180)*

This later chapter builds upon the concepts introduced here, particularly: None, __main__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^93]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __main__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Securing Your Services** *(pp.181–202)*

This later chapter builds upon the concepts introduced here, particularly: None, __name__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^94]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __name__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Bringing It All Together** *(pp.204–238)*

This later chapter builds upon the concepts introduced here, particularly: __init__, __main__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^95]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts __init__, __main__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 6: Monitoring Your Services

*Source: Python Microservices Development, pages 151–180*

### Chapter Summary
Covers monitoring strategies for microservices including centralizing logs with Graylog, sending logs to external services, and metrics collection. Details performance monitoring, alerting systems, and observability practices for distributed microservice architectures. [^96]

### Concept-by-Concept Breakdown
#### **None** *(p.176)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.176, lines 19–26)*:
```
    def _probe():
        info = {'cpu_percent': psutil.cpu_percent(interval=None)}
        logger.info(json.dumps(info))
        loop.call_later(1., _probe)
    loop.add_signal_handler(signal.SIGINT, _exit)
    loop.add_signal_handler(signal.SIGTERM, _exit)
    handler = graypy.GELFHandler('localhost', 12201)
    logger.addHandler(handler)
```
[^97]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.158)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.158, lines 2–9)*:
```
[ 144 ]
    if __name__ == '__main__':
        app.run()
Publish/subscribe
The previous pattern has workers that handle specific topics of messages, and the messages
consumed by a worker are completely gone from the queue. We even added code to
acknowledge that the message was consumed.
When you want a message to be published to several workers, the Publish/Subscribe
```
[^98]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.179)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.179, lines 4–11)*:
```
maxlen=5))
                g.timers[func.__name__].append(time.time() - start)
        return _timeit
    @timeit
    def fast_stuff():
        time.sleep(.001)
    @timeit
    def some_slow_stuff():
```
[^99]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.166)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.166, lines 20–27)*:
```
    def email_errors(func):
        def _email_errors(*args, **kw):
            try:
                return func(*args, **kw)
            except Exception:
                logger.exception('A problem has occured')
                raise
    return _email_errors
```
[^100]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.162)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.162, lines 2–9)*:
```
[ 148 ]
This module implements a Celery task named echo that will echo back a string. To
configure pytest to use it, you need to implement the celery_config and
celery_includes fixtures:
    import pytest
    @pytest.fixture(scope='session')
    def celery_config():
        return {
```
[^101]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 27 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.160)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.160, lines 21–28)*:
```
            res = self.app.get('/api')
            self.assertEqual(res.json['result']['some'], 'data')
Using this adapter offers the ability to manually register responses through register_uri
for some given endpoints on the remote service (here h t t p ://127. 0. 0. 1:5000/a p i ). The
adapter will intercept the call and immediately return the mocked value.
In the test_api() test, it will let us try out the application view and make sure it uses the
provided JSON data when it calls the external service.
The requests-mock will also let you match requests using regular expressions, so it's a
```
[^102]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.151)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.151, lines 15–22)*:
```
useful.
The next section will focus on asynchronous calls; everything your microservice can do that
goes beyond the request-response pattern.
Asynchronous calls
In microservice architectures, asynchronous calls play a fundamental role when a process
that used to be performed in a single application now implicates several microservices.
Asynchronous calls can be as simple as a separate thread or process within a microservice
app, that's getting some work to be done and perform it without interfering with the HTTP
```
[^103]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.176)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.176, lines 6–13)*:
```
Graylog continuously.
In the following example, an asyncio loop sends the CPU usage in percent every second to
Graylog:
    import psutil
    import asyncio
    import signal
    import graypy
    import logging
```
[^104]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.174)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.174, lines 8–15)*:
```
This information is usually stored inside app.session in our microservices, and we can
use a logging.Filter class to add it in each logging record sent to Graylog:
    from flask import session
    import logging
    class InfoFilter(logging.Filter):
        def filter(self, record):
            record.username = session.get('username', 'Anonymous')
            return True
```
[^105]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.155)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.155, lines 24–31)*:
```
        finally:
            connection.close()
    # sending a message about race 34
    message('race.34', 'We have some results!')
    # training 12
    message('training.12', "It's time to do your long run")
These RPC calls will end up adding one message respectively in the race and training
queues. A Race worker script that waits for news about races would look like this:
```
[^106]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.178)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.178, lines 20–27)*:
```
    import random
    from collections import defaultdict, deque
    from flask import Flask, jsonify, g
    app = Flask(__name__)
    class Encoder(json.JSONEncoder):
        def default(self, obj):
            base = super(Encoder, self).default
            # specific encoder for the timed functions
```
[^107]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Decorator** *(p.161)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.161, lines 21–27)*:
```
The following is an example of such a file. Notice that we don't create a Celery instance--but
use the @shared_tasks decorator to mark functions as being celery tasks:
    from celery import shared_task
    import unittest
    @shared_task(bind=True, name='echo')
    def echo(app, msg):
        return msg
```
[^108]
**Annotation:** This excerpt demonstrates 'decorator' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.179)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.179, lines 2–9)*:
```
[ 165 ]
                    g.timers = defaultdict(functools.partial(deque,
maxlen=5))
                g.timers[func.__name__].append(time.time() - start)
        return _timeit
    @timeit
    def fast_stuff():
        time.sleep(.001)
```
[^109]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Dictionary** *(p.175)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.175, lines 10–17)*:
```
and leak it on every call.
The code uses memory without care. For example, a dictionary that's used as an
ad hoc memory cache can grow indefinitely over the days unless there's an upper
limit by design.
There's simply not enough memory allocated to the service--the server is getting
too many requests or is too weak for the job.
It's important to be able to track memory usage over time to find out about these issues
before it impacts users.
```
[^110]
**Annotation:** This excerpt demonstrates 'dictionary' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.167)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.167, lines 21–28)*:
```
But Sentry is focused on errors and is not well suited for general logging. If you want to get
logs other than errors, you need to use something else.
Another open-source solution is Graylog (h t t p ://g r a y l o g . o r g ), which is a general logging
application that comes with a powerful search engine based on Elasticsearch (h t t p s ://w w w
. e l a s t i c . c o /) where the logs are stored. MongoDB (h t t p s ://w w w . m o n g o d b . c o m /) is also
used to store application data.
Graylog can receive any logs via its custom logging format or alternative formats, such as
plain JSON. It has a built-in collector or can be configured to work with collectors such as
```
[^111]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 7: Securing Your Services** *(pp.181–202)*

This later chapter builds upon the concepts introduced here, particularly: None, __name__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^112]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __name__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Bringing It All Together** *(pp.204–238)*

This later chapter builds upon the concepts introduced here, particularly: __main__, __name__, args.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^113]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts __main__, __name__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Packaging and Running Python** *(pp.239–256)*

This later chapter builds upon the concepts introduced here, particularly: None, __name__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^114]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __name__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 7: Securing Your Services

*Source: Python Microservices Development, pages 181–202*

### Chapter Summary
Focuses on security aspects of microservices including TokenDealer for authentication, web application firewalls, and OpenResty with Lua and nginx. Covers rate limiting, concurrency limiting, data validation, application scope limitation, and using Bandit linter for security scanning. [^115]

### Concept-by-Concept Breakdown
#### **None** *(p.199)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.199, lines 27–34)*:
```
Authorization header, when the code calls the Data Service:
    _TOKEN = None
    def get_auth_header(new=False):
        global _TOKEN
        if _TOKEN is None or new:
            _TOKEN = get_token()
        return 'Bearer ' + _TOKEN
    _dataservice = 'http://localhost:5001'
```
[^116]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.195)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.195, lines 14–21)*:
```
    import jwt
    home = JsonBlueprint('home', __name__)
    def _400(desc):
        exc = HTTPException()
        exc.code = 400
        exc.description = desc
        return error_handling(exc)
    _SECRETS = {'strava': 'f0fdeb1f1584fd5431c4250b2e859457'}
```
[^117]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.190)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.190, lines 3–10)*:
```
The create_token() function calls jwt.decode() with the algorithms
argument to make sure the token is verified with the right algorithm. This
is good practice to prevent attacks where a malicious token can trick the
server into using an unexpected algorithm, as noted in
h t t p s ://a u t h 0. c o m /b l o g /c r i t i c a l - v u l n e r a b i l i t i e s - i n - j s o n - w e b - t o
k e n - l i b r a r i e s
When executing this code, the token is displayed in its compressed and uncompressed
form.
```
[^118]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.182)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.182, lines 6–13)*:
```
generated logs and performance metrics.
Graylog uses Elasticsearch to store all the data, and that choice offers fantastic search
features that will make your life easier to look for what's going on. The ability to add alerts
is also useful for being notified when something's wrong. But deploying Graylog should be
considered carefully. An Elastic Search cluster is heavy to run and maintain once it has a lot
of data.
For your metrics, time-series based systems such as InfluxDB (open source) from
InfluxData (h t t p s ://w w w . i n f l u x d a t a . c o m /) is a faster and lightweight alternative. But it's
```
[^119]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 13 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.202)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.202, lines 17–24)*:
```
interpreter, yet, very fast. The language offers a complete set of features and has built-in
async features. You can write coroutines directly in vanilla Lua.
For a Python developer, Lua feels quite Pythonic, and you can start to build scripts with it in
a matter of hours once you know the basic syntax. It has functions, classes, and a standard
library that will make you feel at home.
If you install Lua (refer to h t t p ://w w w . l u a . o r g /s t a r t . h t m l ), you can play with the 
language using the Lua Read Eval Print Loop (REPL) exactly like how you would do with
Python:
```
[^120]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.201)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.201, lines 16–23)*:
```
Cross Site Scripting (XSS): This attack happens only on web pages that display
some HTML. The attacker uses some of the query attributes to try to inject their
piece of HTML on the page to trick the user into performing some actions
thinking they are on the legitimate website.
Cross-Site Request Forgery (XSRF/CSRF): This attack is based on attacking a
service by reusing the user's credentials from another website. The typical CSRF
attack happens with POST requests. For instance, a malicious website displays a
link to a user to trick that user to perform the POST request on your site using
```
[^121]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.187)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.187, lines 19–26)*:
```
OeMWz6ahNsf-TKg8LQNdNMnFHNtReb0x3NMs0eY64WA
Each part in the token above is separated by a line break for display
purpose. The original token is a single line.
And if we use Python to decode it:
>>> import base64
>>> def decode(data):
...     # adding extra = for padding if needed
...     pad = len(data) % 4
```
[^122]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.202)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.202, lines 19–26)*:
```
For a Python developer, Lua feels quite Pythonic, and you can start to build scripts with it in
a matter of hours once you know the basic syntax. It has functions, classes, and a standard
library that will make you feel at home.
If you install Lua (refer to h t t p ://w w w . l u a . o r g /s t a r t . h t m l ), you can play with the 
language using the Lua Read Eval Print Loop (REPL) exactly like how you would do with
Python:
$ lua
Lua 5.1.5  Copyright (C) 1994-2012 Lua.org, PUC-Rio
```
[^123]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Coroutine** *(p.202)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.202, lines 17–24)*:
```
interpreter, yet, very fast. The language offers a complete set of features and has built-in
async features. You can write coroutines directly in vanilla Lua.
For a Python developer, Lua feels quite Pythonic, and you can start to build scripts with it in
a matter of hours once you know the basic syntax. It has functions, classes, and a standard
library that will make you feel at home.
If you install Lua (refer to h t t p ://w w w . l u a . o r g /s t a r t . h t m l ), you can play with the 
language using the Lua Read Eval Print Loop (REPL) exactly like how you would do with
Python:
```
[^124]
**Annotation:** This excerpt demonstrates 'coroutine' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.195)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.195, lines 15–22)*:
```
    home = JsonBlueprint('home', __name__)
    def _400(desc):
        exc = HTTPException()
        exc.code = 400
        exc.description = desc
        return error_handling(exc)
    _SECRETS = {'strava': 'f0fdeb1f1584fd5431c4250b2e859457'}
    def is_authorized_app(client_id, client_secret):
```
[^125]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.186)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.186, lines 10–17)*:
```
token-based authentication works from the ground. If you understand the next section
correctly, everything else in OAuth2 should be easier to grasp.
Token-based authentication
As we said earlier, when a service wants to get access to another service without any user
intervention, we can use a CCG flow.
The idea behind CCG is that a service can authenticate to an authentication service exactly
like a user would do, and ask for a token that it can then use to authenticate against other
services.
```
[^126]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.182)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.182, lines 13–20)*:
```
InfluxData (h t t p s ://w w w . i n f l u x d a t a . c o m /) is a faster and lightweight alternative. But it's
not meant to store raw logs and exceptions.
So if you just care about performance metrics and exceptions, maybe a good solution would
be to use a combination of tools: Sentry for your exceptions and InfluxDB for tracking
performances. In any case, as long as your applications and web servers generate logs and
metrics via UDP, it makes it easier to move from one tool to another.
The next chapter will focus on another important aspect of microservices development: how
to secure your APIs, offer some authentication solutions, and avoid fraud and abuse.
```
[^127]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.182)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.182, lines 13–20)*:
```
InfluxData (h t t p s ://w w w . i n f l u x d a t a . c o m /) is a faster and lightweight alternative. But it's
not meant to store raw logs and exceptions.
So if you just care about performance metrics and exceptions, maybe a good solution would
be to use a combination of tools: Sentry for your exceptions and InfluxDB for tracking
performances. In any case, as long as your applications and web servers generate logs and
metrics via UDP, it makes it easier to move from one tool to another.
The next chapter will focus on another important aspect of microservices development: how
to secure your APIs, offer some authentication solutions, and avoid fraud and abuse.
```
[^128]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.192)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.192, lines 16–23)*:
```
writing RSA key
These three calls generate four files:
The cert.pem file has the certificate
The pubkey.pem file has the public key extracted from the certificate
The key.pem file has the RSA private key, encrypted
The privkey.pem file has the RSA private key, in clear
RSA stands for Rivest, Shamir, and Adleman, the three authors. The RSA
encryption algorithm generates crypto keys that can go up to 4,096 bytes
```
[^129]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.191)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.191, lines 3–10)*:
```
These certificates are issued by a Certificate Authority (CA), and when your browser opens
a page that presents a certificate, it has to be published from one of the CAs supported by
the browser.
The reason why CA exists is to limit the risk of compromised certificates by having a
limited number of trusted entities that generates and manages them, independently from
the companies that use them.
Since anyone can create a self-signed certificate in a shell, it would be quite easy to end up
in a world where you don't know if you can trust a certificate. If the certificate is issued by
```
[^130]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 8: Bringing It All Together** *(pp.204–238)*

This later chapter builds upon the concepts introduced here, particularly: __name__, argument, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^131]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts __name__, argument appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Packaging and Running Python** *(pp.239–256)*

This later chapter builds upon the concepts introduced here, particularly: None, __name__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^132]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __name__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: Deploying on Heroku** *(pp.257–270)*

This later chapter builds upon the concepts introduced here, particularly: None, __name__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^133]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __name__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 8: Bringing It All Together

*Source: Python Microservices Development, pages 204–238*

### Chapter Summary
Demonstrates building a complete application by integrating frontend (ReactJS) with Flask backend. Covers JSX syntax, React components, using Bower/npm/Babel, Cross-Origin Resource Sharing (CORS), authentication and authorization flows, and interacting with external services like Strava. [^134]

### Concept-by-Concept Breakdown
#### **Utf-8** *(p.220)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.220, lines 12–19)*:
```
      <head lang="en">
        <meta charset="UTF-8">
      </head>
      <body>
        <div id="content"></div>
        <script src="/static/react/react.min.js"></script>
        <script src="/static/react-dom.min.js"></script>
        <script src="/static/babel/browser.min.js"></script>
```
[^135]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.209)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.209, lines 11–18)*:
```
    class Extra(object):
        def __init__(self, data):
            self.data = data
    @app.route('/')
    def my_microservice():
        user_id = request.args.get('user_id', 'Anynomous')
        tmpl = _TEMPLATE % user_id
        return render_template_string(tmpl, extra=Extra('something'))
```
[^136]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.215)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.215, lines 37–39)*:
```
   Location: flask_app.py:15
14 if __name__ == '__main__':
15     app.run(debug=True)
```
[^137]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.225)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.225, lines 14–21)*:
```
    from flask import Flask, render_template,
    app = Flask(__name__)
    @app.route('/')
    def index():
        return render_template('index.html')
    if __name__ == '__main__':
        app.run()
Thanks to Flask's convention on static assets, all the files contained inside the static/
```
[^138]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.218)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.218, lines 17–23)*:
```
Tools like Facebook's ReactJS (h t t p s ://f a c e b o o k . g i t h u b . i o /r e a c t /) provide high-level
APIs to avoid manipulating the DOM directly, and offer a level of abstraction, which makes
client-side web development as comfortable as building Flask applications.
That said, there is a new JS framework every other week, and it is hard to decide which one
should be used. AngularJS (h t t p s ://a n g u l a r j s . o r g /) used to be the coolest toy, and now
it seems many developers have switched to implement most of their application UIs with
plain ReactJS. Moreover, maybe later in 2017, another new player will be popular.
```
[^139]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.209)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.209, lines 15–22)*:
```
    def my_microservice():
        user_id = request.args.get('user_id', 'Anynomous')
        tmpl = _TEMPLATE % user_id
        return render_template_string(tmpl, extra=Extra('something'))
By doing this preformatting on the template with a raw %s, the view creates a huge security
hole in the app, since it allows attackers to inject what they want in the Jinja script before it
gets executed.
In the following example, the user_id variable security hole is exploited to read the value
```
[^140]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.210)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.210, lines 27–34)*:
```
This can be prevented by quoting any value used to build raw SQL queries. In PyMySQL,
you just need to pass the values to the execute argument to avoid this problem:
    def get_user(user_id):
        query = 'select * from user where id = %s'
        with connection.cursor() as cursor:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
        return result
```
[^141]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.222)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.222, lines 2–9)*:
```
[ 208 ]
The props array is populated when the Run instance is created, and that is what happens in
the render() method of the Runs class. The runNode variable iterates through the
Runs.props.data list, which contains a list of runs.
That is our last piece of the puzzle. We want to instantiate a Runs class, and put a list of
runs to be rendered by React in its props.data list.
In our Runnerly app, this list can be provided by the microservice that publishes runs, and
we can create another React class, which loads this list asynchronously using an
```
[^142]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.233)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.233, lines 3–10)*:
```
While it is always safer to start with a conservative approach, let's think for a minute how a
split would impact our design. If the dashboard is on its own, it needs to drive DataService
to create and change users' info in DataService. This means that DataService needs to
expose some HTTP APIs to do this. The biggest risk of exposing a database via HTTP is that
whenever it changes, the API might get impacted.
However, that risk can be limited if the exposed endpoints hide the database structure as
much as possible, the opposite of CRUD-like APIs.
For example, the API to create a user in DataService could be a POST that just asks for the
```
[^143]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 25 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.208)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.208, lines 14–21)*:
```
Let's look at how to implement these principles in practice.
Asserting incoming data
The first principle, assert incoming data, just means that your application should not
blindly execute incoming requests without making sure what will be the impact.
For instance, if you have an API that will let a caller delete a line in a database, you need to
make sure the caller is allowed to do it. This is why we've added authentication and
authorization earlier in this chapter.
But there are other ways to breach in. For example, if you have a Flask view that grabs
```
[^144]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.222)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.222, lines 8–15)*:
```
In our Runnerly app, this list can be provided by the microservice that publishes runs, and
we can create another React class, which loads this list asynchronously using an
Asynchronous JavaScript and XML (AJAX) pattern via an HxmlHttpRequest class.
That is what happens in the loadRunsFromServer() method in the following example.
The code calls the server to get the data by making a GET request on the URL set in the
props, and sets the value of props.data by calling the setState() method.
    var RunsBox = React.createClass( {
      loadRunsFromServer: function()  {
```
[^145]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.209)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.209, lines 29–32)*:
```
http://jinja.pocoo.org/docs/latest/sandbox/. This sandbox will reject any access to 
methods and attributes from the object being evaluated. For instance, if you're passing a
callable in your template, you will be sure that its attributes such as __class__ cannot be
used.
```
[^146]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.216)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.216, lines 18–25)*:
```
us the ability to limit what and for how long a caller can do on one of the microservices.
When used with public/private keys, it also prevents an attacker that breaks into one service
to break the whole app, as long as it's not the token issuer that's compromised.
Beyond system-level firewall rules, a Web Application Framework is also a good way to
prevent some fraud and abuse on your endpoints and is very easy to do with a tool such as
OpenResty, thanks to the power of the Lua programming language.
OpenResty is also an excellent way to empower and speed up your microservices by doing
a few things at the web server level when it does not need to be done within the Flask
```
[^147]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.221)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.221, lines 5–12)*:
```
are called for rendering parts of the page.
For example, if you want to display a list of runs, you can create a Run class that is in charge
of rendering a single run given its values, and a Runs class that iterates through a list of
runs, and call the Run class to render each item.
Each class is created with the React.createClass() function, which receives a mapping
containing the future class methods. The createClass() function generates a new class,
and sets a props attribute to hold some properties alongside the provided methods.
In the following example, in a new JavaScript file we define a Run class with a render()
```
[^148]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 13 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class Method** *(p.221)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.221, lines 9–16)*:
```
Each class is created with the React.createClass() function, which receives a mapping
containing the future class methods. The createClass() function generates a new class,
and sets a props attribute to hold some properties alongside the provided methods.
In the following example, in a new JavaScript file we define a Run class with a render()
function, which returns a <div> tag, and a Runs class:
    var Run = React.createClass( {
      render: function()  {
        return (
```
[^149]
**Annotation:** This excerpt demonstrates 'class method' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 9: Packaging and Running Python** *(pp.239–256)*

This later chapter builds upon the concepts introduced here, particularly: __init__, __name__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^150]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts __init__, __name__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: Deploying on Heroku** *(pp.257–270)*

This later chapter builds upon the concepts introduced here, particularly: __main__, __name__, args.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^151]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts __main__, __name__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Deploying on AWS** *(pp.271–334)*

This later chapter builds upon the concepts introduced here, particularly: __init__, __name__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^152]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts __init__, __name__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 9: Packaging and Running Python

*Source: Python Microservices Development, pages 239–256*

### Chapter Summary
Covers packaging Python microservices, managing dependencies, creating distributable packages, and running Python applications in production. Details best practices for packaging, dependency management, and deployment preparation. [^153]

### Concept-by-Concept Breakdown
#### **None** *(p.255)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.255, lines 4–11)*:
```
2 and 3 if your code is compatible with both, with no extra steps (like a 2 to 3 conversion).
Without the flag, a runnerly_tokendealer-0.1.0-py3-none-any.whl file would have
been created, indicating that the release works only for Python 3.
In case you have some C extensions, bdist_wheel will detect it and create a platform-
specific distribution with the compiled extension. In that case, none in the filename is
replaced by the platform.
Creating platform-specific releases is fine if your C extensions are not linking to specific
system libraries. If they do, there are good chances your binary release will not work
```
[^154]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.256)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.256, lines 9–16)*:
```
To do this, you just need to create the same top-level directory in every project, with the
__init__.py file containing and prefixing all absolute imports with the top-level name.
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
For example, in Runnerly, if we decide to release everything under the same namespace,
each project can have the same top-level package name. For example, in the token dealer, it 
could be as follows:
runnerly
```
[^155]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.256)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.256, lines 11–18)*:
```
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
For example, in Runnerly, if we decide to release everything under the same namespace,
each project can have the same top-level package name. For example, in the token dealer, it 
could be as follows:
runnerly
__init__.py: Contains the extend_path call
tokendealer/
```
[^156]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.243)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.243, lines 17–24)*:
```
obviously not enough information to describe your project.
Metadata fields are set through setup() arguments. Some of them match directly with the
name of the metadata, some don't.
The following is the minimal set of arguments you should use for your microservices
projects:
name: The name of the package, should be a short lowercase name
version: The version of the project, as defined in PEP 440
url: A URL for the project; can be its repository or home page
```
[^157]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.251)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.251, lines 5–12)*:
```
than another one.
Early software used schemes based on the date of release, like 20170101 if your software is
released on 1st January 2017. But that scheme won't work anymore if you do branch
releases. For instance, if your software has a version 2, which is backward incompatible,
you might start to release updates for version 1 in parallel of releases for version 2. In that
case, using dates will make some of your version 1 releases appear as if they were more
recent than some version 2 release.
Some software combine incremental versions and dates for that reason, but it became
```
[^158]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 28 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.252)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.252, lines 23–30)*:
```
the existing API
MINOR is incremented when you add new features that don't break the existing
API
PATCH is incremented just for bug fixes
Being strict about this scheme with the 0.x.x series when the software is in its early phase
does not make much sense, because you will do a lot of backward incompatible changes,
and your MAJOR version would reach a high number in no time.
The 1.0.0 release is often emotionally charged for developers.
```
[^159]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.245)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.245, lines 9–16)*:
```
add, alongside your setup.py file, a LICENCE file with the official text of that license.
The classifiers option is probably the most painful one to write. You need to use strings
from h t t p s ://p y p i . p y t h o n . o r g /p y p i ?%3A a c t i o n =l i s t _ c l a s s i f i e r s , which classify your
project. The three most common classifiers that developers use are the list of supported
Python versions, the license (which duplicates and should match the license option), and
the development status, which is a hint about the maturity of the project.
Keywords are a good way to make your project visible if you publish it to the Python
Package Index. For instance, if you are creating a Flask microservice, you should use flask
```
[^160]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.252)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.252, lines 7–14)*:
```
Here's an example of a sorted list of versions for a project that will work in Python, and
which will be close to SemVer:
9.0
0.0a1
0.0a2
0.0b1
0.0rc1
0.0
```
[^161]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.247)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.247, lines 27–32)*:
```
development, and a prod-requirements.txt, which has production-specific things. The
format allows inheritance to help you manage requirements files' collections.
But using requirements files adds a new problem. It duplicates some of the information
contained in thesetup.py file's install_requires section.
To solve this new issue, some developers make a distinction between dependencies defined
for their Python libraries and the one defined for their Python applications.
```
[^162]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Compiled** *(p.254)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.254, lines 14–21)*:
```
Source releases are good enough when you don't have any extension that needs to be
compiled. If you do, the target system will need to compile them again when the
installation happens. That means the target system needs to have a compiler, which is not
always the case.
Another option is to precompile and create binary distributions for each target system.
Distutils has several bdist_xxx commands to do it, but they are not really maintained
anymore. The new format to use is the Wheel format as defined in PEP 427. The Wheel
format is a ZIP file containing all the files that will be deployed on the target system,
```
[^163]
**Annotation:** This excerpt demonstrates 'compiled' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.241)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.241, lines 18–25)*:
```
Before we start to look at the tools that should be used, we need to go through a few
definitions to avoid any confusion.
A few definitions
When we talk about packaging Python projects, a few terms can be confusing, because their
definitions have evolved over time, and also because they can mean slightly different things
outside the Python world.
We need to define, what's a Python package, a Python project, a Python library, and a
Python application. They are defined as follows:
```
[^164]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.249)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.249, lines 17–24)*:
```
The simplest way to fix this issue is to leave the dependencies unpinned in the setup.py
file and pinned in the requirements.txt file. That way, PIP can install the latest version
for each package, and when you deploy, specifically in stage or production, you can refresh
the versions by running the pip install -r requirements.txt command. PIP will
then upgrade/downgrade all the dependencies to match the versions, and in case you need
to, you can tweak them in the requirements file.
To summarize, defining dependencies should be done in each project's setup.py file, and
requirements files can be provided with pinned dependencies as long as you have a
```
[^165]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 15 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.240)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.240, lines 12–19)*:
```
In this chapter, we are going to look at how we can leverage the packaging tools to run all
microservices from the same environment, and then how to run them all from a single
command-line interface by using a dedicated process manager.
However, first, let's look at how to package your projects, and which tools should be
utilized.
The packaging toolchain
Python has come a long way in the past ten years on packaging. Numerous Python
Enhancement Proposals (PEPs) were written to improve how to install, release, and
```
[^166]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.245)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.245, lines 23–30)*:
```
are callables that can be used as plugins once the project is installed in Python. The most
common entry point type is the console script. When you add functions in that section, a
command-line script will be installed alongside the Python interpreter, and the function
hooked to it via the entry point. This is a good way to create a Command-Line Interface
(CLI) for your project. In the example, mycli should be directly reachable in the shell when
the project is installed. Python's Distutils has a similar feature, but the one in Setuptools
does a better job, because it allows you to point to a specific function.
Lastly, install_requires lists all the dependencies. This list of Python projects the
```
[^167]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.243)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.243, lines 7–14)*:
```
everyone uses them. So setup.py is going to stick around for years.
A very common mistake when creating the setup.py file is to import your package in it
when you have third-party dependencies. If a tool like PIP tries to read the metadata by
running setup.py, it might raise an import error before it has a chance to list all the
dependencies to install.
The only dependency you can afford to import directly in your setup.py file is Setuptools,
because you can make the assumption that anyone trying to install your project is likely to
have it in their environment.
```
[^168]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 10: Deploying on Heroku** *(pp.257–270)*

This later chapter builds upon the concepts introduced here, particularly: None, __name__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^169]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __name__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Deploying on AWS** *(pp.271–334)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^170]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 10: Deploying on Heroku

*Source: Python Microservices Development, pages 257–270*

### Chapter Summary
Explains deploying microservices on Heroku platform, covering the full stack with OpenResty, Circus, and Flask. Introduces Docker-based deployments, Docker Compose, clustering, and provisioning strategies for cloud deployment. [^171]

### Concept-by-Concept Breakdown
#### **None** *(p.263)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.263, lines 8–15)*:
```
                                         Dataservice')
        parser.add_argument('--fd', type=int, default=None)
        parser.add_argument('--config-file', help='Config file',
                            type=str, default=None)
        args = parser.parse_args(args=args)
        app = create_app(args.config_file)
        host = app.config.get('host', '0.0.0.0')
        port = app.config.get('port', 5000)
```
[^172]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.259)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.259, lines 11–18)*:
```
        app.run(debug=debug, host=host, port=port)
    if __name__ == "__main__":
        main()
This approach offers a lot of flexibility. In order to make that script a console script, you
need to pass it to your setup class's function via the entry_points option as follows:
    from setuptools import setup, find_packages
    from runnerly.dataservice import __version__
    setup(name='runnerly-data',
```
[^173]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.259)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.259, lines 11–18)*:
```
        app.run(debug=debug, host=host, port=port)
    if __name__ == "__main__":
        main()
This approach offers a lot of flexibility. In order to make that script a console script, you
need to pass it to your setup class's function via the entry_points option as follows:
    from setuptools import setup, find_packages
    from runnerly.dataservice import __version__
    setup(name='runnerly-data',
```
[^174]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argparse** *(p.258)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.258, lines 18–25)*:
```
start to add environment variables.
Another option is to create our own launcher using the argparse module (h t t p s ://d o c s . p y
t h o n . o r g /3/l i b r a r y /a r g p a r s e . h t m l ), so that we can add for each microservice any option
we want.
The following example is a full working launcher, which will run a Flask application via an
argparse-based command-line script. It takes a single option, -config-file, which is the
configuration file that contains everything needed by the microservice to run.
    import argparse
```
[^175]
**Annotation:** This excerpt demonstrates 'argparse' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.263)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.263, lines 5–12)*:
```
    from chaussette.server import make_server
    def main(args=sys.argv[1:]):
        parser = argparse.ArgumentParser(description='Runnerly
                                         Dataservice')
        parser.add_argument('--fd', type=int, default=None)
        parser.add_argument('--config-file', help='Config file',
                            type=str, default=None)
        args = parser.parse_args(args=args)
```
[^176]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.258)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.258, lines 16–23)*:
```
Running apps using Flask's command line is fine, but it restricts us to use its interface
options. If we want to pass a few arguments to run our microservice, we would need to
start to add environment variables.
Another option is to create our own launcher using the argparse module (h t t p s ://d o c s . p y
t h o n . o r g /3/l i b r a r y /a r g p a r s e . h t m l ), so that we can add for each microservice any option
we want.
The following example is a full working launcher, which will run a Flask application via an
argparse-based command-line script. It takes a single option, -config-file, which is the
```
[^177]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.258)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.258, lines 5–12)*:
```
Running all microservices
Running a microservice can be done by using the built-in Flask web server. Running the
Flask apps via this script requires to set up an environment variable, which points to the
module that contains the flask application.
In the following example, the application for Runnerly, the dataservice microservice is
located in the app module in runnerly.dataservice and can be launched from the root
directory with this command:
$ FLASK_APP=runnerly/dataservice/app.py bin/flask run
```
[^178]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 15 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.265)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.265, lines 15–22)*:
```
applications locally, and are forced to install much of the software at the system level, it
could be a dealbreaker.
That is where VMs are a great solution to run your applications. In the past ten years, many
software projects that required an elaborate setup to run started to provide ready-to-run
VMs, using tools such as VMWare or VirtualBox. Those VMs included the whole stack, like
prefilled databases. Demos became easily runnable on most platforms with a single
command. That was progress.
However, some of those tools were not fully open source, and they were very slow to run,
```
[^179]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.259)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.259, lines 14–21)*:
```
This approach offers a lot of flexibility. In order to make that script a console script, you
need to pass it to your setup class's function via the entry_points option as follows:
    from setuptools import setup, find_packages
    from runnerly.dataservice import __version__
    setup(name='runnerly-data',
          version=__version__,
          packages=find_packages(),
          include_package_data=True,
```
[^180]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Debugging** *(p.264)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.264, lines 5–12)*:
```
Circus also offers options to redirect the stdout and stderr streams to
log files to facilitate the debugging and numerous other features you can
find at h t t p s ://c i r c u s . r e a d t h e d o c s . i o /e n /l a t e s t /f o r - o p s /c o n f i g u r
a t i o n /.
Summary
In this chapter, we've looked at how to package, release, and distribute each microservice.
The current state of the art in Python packaging still requires some knowledge about the
legacy tools, and this will be the case for some years until all the ongoing work in Python
```
[^181]
**Annotation:** This excerpt demonstrates 'debugging' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.263)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.263, lines 5–12)*:
```
    from chaussette.server import make_server
    def main(args=sys.argv[1:]):
        parser = argparse.ArgumentParser(description='Runnerly
                                         Dataservice')
        parser.add_argument('--fd', type=int, default=None)
        parser.add_argument('--config-file', help='Config file',
                            type=str, default=None)
        args = parser.parse_args(args=args)
```
[^182]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Descriptor** *(p.261)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.261, lines 29–34)*:
```
dedicated sections, and for each one of them, the number of processes you want to use.
Circus can also bind sockets, and let the forked process use them via their file descriptors.
When a socket is created on your system, it uses a file descriptor (FD), which is a system
handle a program can use to reach a file or an I/O resource like sockets. A process that is
forked from another one inherits all its file descriptors. That is, through this mechanism, all
the processes launched by Circus can share the same sockets.
```
[^183]
**Annotation:** This excerpt demonstrates 'descriptor' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.263)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.263, lines 23–30)*:
```
                httpd.serve_forever()
            else:
                app.run(debug=debug, host=host, port=port)
        if not debug:
            runner()
        else:
            from werkzeug.serving import run_with_reloader
            run_with_reloader(runner)
```
[^184]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.259)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.259, lines 4–11)*:
```
        args = parser.parse_args(args=args)
        app = create_app(args.config_file)
        host = app.config.get('host', '0.0.0.0')
        port = app.config.get('port', 5000)
        debug = app.config.get('DEBUG', False)
        signal.signal(signal.SIGINT, _quit)
        signal.signal(signal.SIGTERM, _quit)
        app.run(debug=debug, host=host, port=port)
```
[^185]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.263)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.263, lines 2–9)*:
```
[ 249 ]
The main() function from the microservice can use the make_server() function from
Chaussette and use it in case an -fd option is passed when launched.
    from chaussette.server import make_server
    def main(args=sys.argv[1:]):
        parser = argparse.ArgumentParser(description='Runnerly
                                         Dataservice')
        parser.add_argument('--fd', type=int, default=None)
```
[^186]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 11: Deploying on AWS** *(pp.271–334)*

This later chapter builds upon the concepts introduced here, particularly: None, __name__, argparse.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^187]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __name__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 11: Deploying on AWS

*Source: Python Microservices Development, pages 271–334*

### Chapter Summary
Comprehensive guide to deploying microservices on AWS, covering AWS services including Route53, ELB, AutoScaling, EC2, Lambda, EBS, S3, RDS, ElasticCache, CloudFront, SES, SQS, SNS, CloudFormation, and ECS. Details AWS deployment basics and best practices for production microservices. [^188]

### Concept-by-Concept Breakdown
#### **Gil** *(p.328)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.328, lines 12–19)*:
```
   URL  24
Gilectomy
   about  29
   URL  29
GitHub
   URL  88
GitLab
   URL  88
```
[^189]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.314)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.314, lines 23–30)*:
```
>>> t = terminal()
>>> t.next()    # call to initialise the generator - similar to send(None)
>>> t.send("echo hey")
hey
>>> t.send("eval 1+1")
2
>>> t.send("exit")
Bye!
```
[^190]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.313)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.313, lines 4–11)*:
```
    class Fibo:
        def __init__(self, max=10):
            self.a, self.b = 0, 1
            self.max = max
            self.count = 0
        def __iter__(self):
            return self
        def next(self):
```
[^191]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.319)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.319, lines 25–30)*:
```
    from sanic import Sanic, response
    app = Sanic(__name__)
    @app.route("/api")
    async def api(request):
        return response.json({'some': 'data'})
    app.run()
```
[^192]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argparse** *(p.324)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.324, lines 40–47)*:
```
Apache Public Licence Version 2 (APL v2)  231
argparse module
   about  244
   URL  244
Association for Computing Machinery (ACM)  21
asynchronous calls
   about  137
   Celery, mocking  147
```
[^193]
**Annotation:** This excerpt demonstrates 'argparse' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.312)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.312, lines 2–9)*:
```
[ 298 ]
As we've seen in Chapter 10, Containerized services, Docker seems to be the new standard
for containerizing applications. But, maybe, other players will become serious alternatives,
like CoreOs's rkt (h t t p s ://c o r e o s . c o m /r k t /). In any case, the maturity of the containers
technology will be reached the day all containers engines are based on a universal standard
to describe images--and that is the goal of organizations such as Open Container Initiative
(OCI) (h t t p s ://w w w . o p e n c o n t a i n e r s . o r g /), which is driven by all the big containers and
cloud players.
```
[^194]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 24 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.326)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.326, lines 4–11)*:
```
   Bandit linter, using  199, 200, 202
   incoming data, asserting  194, 195, 196, 197,
198
Command-Line Interface (CLI)  231
Common Gateway Interface (CGI)  22
components, monolithic application
   Authentication  15
   Booking UI  14
```
[^195]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.316)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.316, lines 3–10)*:
```
The difference is that you can't use the await call to call a generator (yet).
The async keyword marks a function, a for or a with loop, as being a native coroutine, and
if you try to use that function, you will not retrieve a generator but a coroutine object.
The native coroutine type that was added in Python is like a fully symmetric generator, but
all the back and forth is delegated to an event loop, which is in charge of coordinating the
execution.
In the example that follows, the asyncio library is used to run main(), which, in turn, calls
several coroutines in parallel:
```
[^196]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 13 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.316)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.316, lines 8–15)*:
```
execution.
In the example that follows, the asyncio library is used to run main(), which, in turn, calls
several coroutines in parallel:
    import asyncio
    async def compute():
        for i in range(5):
            print('compute %d' % i)
            await asyncio.sleep(.1)
```
[^197]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.316)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.316, lines 2–9)*:
```
[ 302 ]
The difference is that you can't use the await call to call a generator (yet).
The async keyword marks a function, a for or a with loop, as being a native coroutine, and
if you try to use that function, you will not retrieve a generator but a coroutine object.
The native coroutine type that was added in Python is like a fully symmetric generator, but
all the back and forth is delegated to an event loop, which is in charge of coordinating the
execution.
In the example that follows, the asyncio library is used to run main(), which, in turn, calls
```
[^198]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.314)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.314, lines 16–23)*:
```
                print("Bye!")
                break
            elif msg.startswith('echo'):
                print(msg.split('echo ', 1)[1])
            elif msg.startswith('eval'):
                print(eval(msg.split('eval', 1)[1]))
When instantiated, this generator can receive data via its send() method:
>>> t = terminal()
```
[^199]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.317)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.317, lines 14–21)*:
```
language.
The asyncio library is inspired by Twisted, and offers classes that mimic Twisted transports
and protocols. Building a network application based on these consists of combining a
transport class (like TCP) and a protocol class (such as HTTP), and using callbacks to
orchestrate the execution of the various parts.
But, with the introduction of native coroutines, callback-style programming is less
appealing, since it's much more readable to orchestrate the execution order via await calls.
You can use coroutine with asyncio protocol and transport classes, but the original design
```
[^200]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.291)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.291, lines 13–20)*:
```
your users are spread all over the world. Amazon caches the files, and makes them
available with the minimum latency possible by routing the client's requests to the closest
server. A CDN is what you need to use to serve video, CSS, and JS files--one thing to look
at, though, is the cost. If you have a few assets to serve for your microservice, it might be
simpler to serve them directly from your EC2 instance.
Messaging - SES, SQS, and SNS
For all messaging needs, AWS provides these three major services:
Simple Email Service (SES): An email service
```
[^201]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Coroutine** *(p.317)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.317, lines 12–19)*:
```
asynchronous programs based on an event loop.
The library predates the introduction of async, await, and native coroutines in the
language.
The asyncio library is inspired by Twisted, and offers classes that mimic Twisted transports
and protocols. Building a network application based on these consists of combining a
transport class (like TCP) and a protocol class (such as HTTP), and using callbacks to
orchestrate the execution of the various parts.
But, with the introduction of native coroutines, callback-style programming is less
```
[^202]
**Annotation:** This excerpt demonstrates 'coroutine' as it appears in the primary text. The concept occurs 10 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Debugging** *(p.325)*

**Verbatim Educational Excerpt** *(Python Microservices Dev, p.325, lines 45–52)*:
```
   configuration  54
   debugging  57
   error handling  57
   extensions  51
   globals  48
   middlewares  51
   session object  47
   signals  49
```
[^203]
**Annotation:** This excerpt demonstrates 'debugging' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---


---

### **Footnotes**

[^1]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 8, lines 1–25).
[^2]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 22, lines 7–14).
[^3]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 26, lines 2–9).
[^4]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 13, lines 13–20).
[^5]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 12, lines 19–26).
[^6]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 10, lines 39–46).
[^7]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 27, lines 2–9).
[^8]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 30, lines 20–27).
[^9]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 21, lines 18–20).
[^10]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 14, lines 51–58).
[^11]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 11, lines 9–16).
[^12]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 29, lines 28–35).
[^13]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 18, lines 15–22).
[^14]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 11, lines 9–16).
[^15]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 18, lines 14–21).
[^16]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 31, lines 12–19).
[^17]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 33, lines 1–1).
[^18]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 65, lines 1–1).
[^19]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 95, lines 1–1).
[^20]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 33, lines 1–25).
[^21]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 43, lines 21–28).
[^22]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 60, lines 20–27).
[^23]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 52, lines 33–37).
[^24]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 50, lines 16–23).
[^25]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 50, lines 12–19).
[^26]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 55, lines 5–12).
[^27]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 60, lines 5–12).
[^28]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 42, lines 2–9).
[^29]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 42, lines 16–23).
[^30]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 42, lines 2–9).
[^31]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 42, lines 3–10).
[^32]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 58, lines 18–25).
[^33]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 42, lines 9–16).
[^34]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 53, lines 3–10).
[^35]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 41, lines 6–13).
[^36]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 65, lines 1–1).
[^37]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 95, lines 1–1).
[^38]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 121, lines 1–1).
[^39]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 65, lines 1–25).
[^40]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 79, lines 8–11).
[^41]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 69, lines 2–9).
[^42]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 76, lines 22–29).
[^43]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 66, lines 3–10).
[^44]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 72, lines 26–33).
[^45]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 82, lines 10–17).
[^46]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 93, lines 3–10).
[^47]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 86, lines 5–12).
[^48]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 90, lines 10–17).
[^49]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 65, lines 16–23).
[^50]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 90, lines 11–18).
[^51]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 69, lines 39–40).
[^52]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 79, lines 10–11).
[^53]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 82, lines 5–12).
[^54]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 67, lines 27–34).
[^55]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 95, lines 1–1).
[^56]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 121, lines 1–1).
[^57]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 151, lines 1–1).
[^58]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 95, lines 1–25).
[^59]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 118, lines 3–10).
[^60]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 102, lines 16–23).
[^61]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 99, lines 14–21).
[^62]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 99, lines 10–17).
[^63]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 117, lines 23–30).
[^64]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 113, lines 2–9).
[^65]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 115, lines 8–15).
[^66]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 103, lines 19–26).
[^67]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 113, lines 3–10).
[^68]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 118, lines 33–40).
[^69]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 117, lines 27–34).
[^70]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 118, lines 4–11).
[^71]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 99, lines 20–27).
[^72]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 106, lines 3–10).
[^73]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 96, lines 10–17).
[^74]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 121, lines 1–1).
[^75]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 151, lines 1–1).
[^76]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 181, lines 1–1).
[^77]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 121, lines 1–25).
[^78]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 127, lines 4–11).
[^79]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 144, lines 7–14).
[^80]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 122, lines 19–26).
[^81]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 138, lines 22–29).
[^82]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 138, lines 15–22).
[^83]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 125, lines 11–18).
[^84]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 122, lines 19–26).
[^85]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 130, lines 6–13).
[^86]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 122, lines 5–12).
[^87]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 135, lines 8–15).
[^88]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 124, lines 24–31).
[^89]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 122, lines 10–17).
[^90]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 141, lines 28–31).
[^91]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 150, lines 30–37).
[^92]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 124, lines 8–15).
[^93]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 151, lines 1–1).
[^94]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 181, lines 1–1).
[^95]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 204, lines 1–1).
[^96]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 151, lines 1–25).
[^97]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 176, lines 19–26).
[^98]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 158, lines 2–9).
[^99]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 179, lines 4–11).
[^100]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 166, lines 20–27).
[^101]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 162, lines 2–9).
[^102]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 160, lines 21–28).
[^103]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 151, lines 15–22).
[^104]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 176, lines 6–13).
[^105]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 174, lines 8–15).
[^106]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 155, lines 24–31).
[^107]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 178, lines 20–27).
[^108]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 161, lines 21–27).
[^109]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 179, lines 2–9).
[^110]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 175, lines 10–17).
[^111]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 167, lines 21–28).
[^112]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 181, lines 1–1).
[^113]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 204, lines 1–1).
[^114]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 239, lines 1–1).
[^115]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 181, lines 1–25).
[^116]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 199, lines 27–34).
[^117]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 195, lines 14–21).
[^118]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 190, lines 3–10).
[^119]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 182, lines 6–13).
[^120]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 202, lines 17–24).
[^121]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 201, lines 16–23).
[^122]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 187, lines 19–26).
[^123]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 202, lines 19–26).
[^124]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 202, lines 17–24).
[^125]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 195, lines 15–22).
[^126]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 186, lines 10–17).
[^127]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 182, lines 13–20).
[^128]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 182, lines 13–20).
[^129]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 192, lines 16–23).
[^130]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 191, lines 3–10).
[^131]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 204, lines 1–1).
[^132]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 239, lines 1–1).
[^133]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 257, lines 1–1).
[^134]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 204, lines 1–25).
[^135]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 220, lines 12–19).
[^136]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 209, lines 11–18).
[^137]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 215, lines 37–39).
[^138]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 225, lines 14–21).
[^139]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 218, lines 17–23).
[^140]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 209, lines 15–22).
[^141]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 210, lines 27–34).
[^142]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 222, lines 2–9).
[^143]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 233, lines 3–10).
[^144]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 208, lines 14–21).
[^145]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 222, lines 8–15).
[^146]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 209, lines 29–32).
[^147]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 216, lines 18–25).
[^148]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 221, lines 5–12).
[^149]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 221, lines 9–16).
[^150]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 239, lines 1–1).
[^151]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 257, lines 1–1).
[^152]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 271, lines 1–1).
[^153]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 239, lines 1–25).
[^154]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 255, lines 4–11).
[^155]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 256, lines 9–16).
[^156]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 256, lines 11–18).
[^157]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 243, lines 17–24).
[^158]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 251, lines 5–12).
[^159]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 252, lines 23–30).
[^160]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 245, lines 9–16).
[^161]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 252, lines 7–14).
[^162]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 247, lines 27–32).
[^163]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 254, lines 14–21).
[^164]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 241, lines 18–25).
[^165]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 249, lines 17–24).
[^166]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 240, lines 12–19).
[^167]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 245, lines 23–30).
[^168]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 243, lines 7–14).
[^169]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 257, lines 1–1).
[^170]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 271, lines 1–1).
[^171]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 257, lines 1–25).
[^172]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 263, lines 8–15).
[^173]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 259, lines 11–18).
[^174]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 259, lines 11–18).
[^175]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 258, lines 18–25).
[^176]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 263, lines 5–12).
[^177]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 258, lines 16–23).
[^178]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 258, lines 5–12).
[^179]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 265, lines 15–22).
[^180]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 259, lines 14–21).
[^181]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 264, lines 5–12).
[^182]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 263, lines 5–12).
[^183]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 261, lines 29–34).
[^184]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 263, lines 23–30).
[^185]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 259, lines 4–11).
[^186]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 263, lines 2–9).
[^187]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 271, lines 1–1).
[^188]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 271, lines 1–25).
[^189]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 328, lines 12–19).
[^190]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 314, lines 23–30).
[^191]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 313, lines 4–11).
[^192]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 319, lines 25–30).
[^193]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 324, lines 40–47).
[^194]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 312, lines 2–9).
[^195]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 326, lines 4–11).
[^196]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 316, lines 3–10).
[^197]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 316, lines 8–15).
[^198]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 316, lines 2–9).
[^199]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 314, lines 16–23).
[^200]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 317, lines 14–21).
[^201]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 291, lines 13–20).
[^202]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 317, lines 12–19).
[^203]: Ziadé, Tarek. *Python Microservices Development*. (JSON `Python Microservices Development.json`, p. 325, lines 45–52).
