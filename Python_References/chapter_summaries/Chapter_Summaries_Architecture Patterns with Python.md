# Comprehensive Python Guidelines — Architecture Patterns with Python (Chapters 1-13)

*Source: Architecture Patterns with Python, Chapters 1-13*

---

## Chapter 1: Domain Modeling

*Source: Architecture Patterns with Python, pages 1–24*

### Chapter Summary
Introduces domain modeling and Domain-Driven Design (DDD) concepts including entities, value objects, and aggregates. Focuses on modeling business logic and domain concepts in Python with proper encapsulation and invariants. [^1]

### Concept-by-Concept Breakdown
#### **None** *(p.20)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.20, lines 11–18)*:
```
evolving requirements.
None of the techniques and patterns we discuss in this book are new,
but they are mostly new to the Python world. And this book isn’t a
replacement for the classics in the field such as Eric Evans’s Domain-
Driven Design or Martin Fowler’s Patterns of Enterprise
Application Architecture (both published by Addison-Wesley
Professional)—which we often refer to and encourage you to go and
read.
```
[^2]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.24)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.24, lines 18–25)*:
```
model free of extraneous dependencies. We build a layer of
abstraction around persistent storage, and we build a service layer
to define the entrypoints to our system and capture the primary use
cases. We show how this layer makes it easy to build thin
entrypoints to our system, whether it’s a Flask API or a CLI.
Some thoughts on testing and abstractions (Chapters 3 and 6)
After presenting the first abstraction (the Repository pattern), we
take the opportunity for a general discussion of how to choose
```
[^3]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.21)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.21, lines 5–12)*:
```
without fear of regression. But it can be hard to get the best
out of our tests: How do we make sure that they run as fast as
possible? That we get as much coverage and feedback from
fast, dependency-free unit tests and have the minimum number
of slower, flaky end-to-end tests?
2. Domain-driven design (DDD) asks us to focus our efforts on
building a good model of the business domain, but how do we
make sure that our models aren’t encumbered with
```
[^4]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 11 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.9)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.9, lines 21–24)*:
```
c. The Alternative: Temporal Decoupling Using
Asynchronous Messaging
d. Using a Redis Pub/Sub Channel for
Integration
```
[^5]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.20)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.20, lines 13–20)*:
```
but they are mostly new to the Python world. And this book isn’t a
replacement for the classics in the field such as Eric Evans’s Domain-
Driven Design or Martin Fowler’s Patterns of Enterprise
Application Architecture (both published by Addison-Wesley
Professional)—which we often refer to and encourage you to go and
read.
But all the classic code examples in the literature do tend to be written
in Java or C++/#, and if you’re a Python person and haven’t used
```
[^6]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.22)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.22, lines 4–11)*:
```
Here are a few things we assume about you, dear reader:
You’ve been close to some reasonably complex Python
applications.
You’ve seen some of the pain that comes with trying to
manage that complexity.
You don’t necessarily know anything about DDD or any of the
classic application architecture patterns.
We structure our explorations of architectural patterns around an
```
[^7]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Closure** *(p.11)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.11, lines 7–14)*:
```
and Java-y?
c. Preparing Handlers: Manual DI with Closures
and Partials
d. An Alternative Using Classes
e. A Bootstrap Script
f. Message Bus Is Given Handlers at Runtime
g. Using Bootstrap in Our Entrypoints
h. Initializing DI in Our Tests
```
[^8]
**Annotation:** This excerpt demonstrates 'closure' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Context Manager** *(p.6)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.6, lines 1–8)*:
```
b. Test-Driving a UoW with Integration Tests
c. Unit of Work and Its Context Manager
i. The Real Unit of Work Uses
SQLAlchemy Sessions
ii. Fake Unit of Work for Testing
d. Using the UoW in the Service Layer
e. Explicit Tests for Commit/Rollback Behavior
f. Explicit Versus Implicit Commits
```
[^9]
**Annotation:** This excerpt demonstrates 'context manager' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.12)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.12, lines 23–24)*:
```
21. C. Swapping Out the Infrastructure: Do Everything
with CSVs
```
[^10]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.11)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.11, lines 16–23)*:
```
Example
i. Define the Abstract and Concrete
Implementations
ii. Make a Fake Version for Your Tests
iii. Figure Out How to Integration Test the
Real Thing
j. Wrap-Up
18. Epilogue
```
[^11]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.18)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.18, lines 14–20)*:
```
all these questions.
Bob ended up a software architect because nobody else on his team
was doing it. He turned out to be pretty bad at it, but he was lucky
enough to run into Ian Cooper, who taught him new ways of writing
and thinking about code.
Managing Complexity, Solving Business
Problems
```
[^12]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Encapsulation** *(p.2)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.2, lines 19–22)*:
```
a. Why Do Our Designs Go Wrong?
b. Encapsulation and Abstractions
c. Layering
d. The Dependency Inversion Principle
```
[^13]
**Annotation:** This excerpt demonstrates 'encapsulation' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Error Handling** *(p.9)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.9, lines 19–24)*:
```
Nouns
b. Error Handling in Distributed Systems
c. The Alternative: Temporal Decoupling Using
Asynchronous Messaging
d. Using a Redis Pub/Sub Channel for
Integration
```
[^14]
**Annotation:** This excerpt demonstrates 'error handling' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.3)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.3, lines 15–22)*:
```
Our Models with Idiomatic Python
ii. Exceptions Can Express Domain
Concepts Too
5. 2. Repository Pattern
a. Persisting Our Domain Model
b. Some Pseudocode: What Are We Going to
Need?
c. Applying the DIP to Data Access
```
[^15]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.3)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.3, lines 15–22)*:
```
Our Models with Idiomatic Python
ii. Exceptions Can Express Domain
Concepts Too
5. 2. Repository Pattern
a. Persisting Our Domain Model
b. Some Pseudocode: What Are We Going to
Need?
c. Applying the DIP to Data Access
```
[^16]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 2: Repository Pattern** *(pp.25–46)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^17]

**Annotation:** Forward reference: Chapter 2 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 3: A Brief Interlude: On Coupling and Abstractions** *(pp.47–58)*

This later chapter builds upon the concepts introduced here, particularly: None, as, class.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^18]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Our First Use Case: Flask API and Service Layer** *(pp.59–86)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^19]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 2: Repository Pattern

*Source: Architecture Patterns with Python, pages 25–46*

### Chapter Summary
Explores the Repository pattern for abstracting data persistence and database access. Covers implementing repositories with SQLAlchemy, the ports and adapters (hexagonal) architecture, and separating domain logic from infrastructure concerns. [^20]

### Concept-by-Concept Breakdown
#### **Gil** *(p.31)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.31, lines 1–8)*:
```
Gigantic thanks also to our Early Release readers for their comments
and suggestions: Ian Cooper, Abdullah Ariff, Jonathan Meier, Gil
Gonçalves, Matthieu Choplin, Ben Judson, James Gregory, Łukasz
Lechowicz, Clinton Roy, Vitorino Araújo, Susan Goodbody, Josh
Harwood, Daniel Butler, Liu Haibin, Jimmy Davies, Ignacio Vergara
Kausel, Gaia Canestrani, Renne Rocha, pedroabi, Ashia Zawaduk,
Jostein Leira, Brandon Rhodes, and many more; our apologies if we
missed you on this list.
```
[^21]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.43)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.43, lines 11–13)*:
```
If you’d like a picture of where we’re going, take a look at Figure I-1,
but don’t worry if none of it makes sense yet! We introduce each box in
the figure, one by one, throughout this part of the book.
```
[^22]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.36)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.36, lines 1–8)*:
```
Encapsulating behavior by using abstractions is a powerful tool for
making code more expressive, more testable, and easier to maintain.
NOTE
In the literature of the object-oriented (OO) world, one of the classic
characterizations of this approach is called responsibility-driven design; it uses
the words roles and responsibilities rather than tasks. The main point is to think
about code in terms of behavior, rather than in terms of data or algorithms.
ABSTRACTIONS AND ABCS
```
[^23]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.36)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.36, lines 12–19)*:
```
The abstraction can just mean “the public API of the thing you’re using”—a function name plus
some arguments, for example.
Most of the patterns in this book involve choosing an abstraction, so
you’ll see plenty of examples in each chapter. In addition, Chapter 3
specifically discusses some general heuristics for choosing
abstractions.
Layering
Encapsulation and abstraction help us by hiding details and protecting
```
[^24]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.26)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.26, lines 3–10)*:
```
what we know from pairing with people, writing code with them, and
learning by doing, and we’d like to re-create that experience as much
as possible for you in this book.
As a result, we’ve structured the book around a single example project
(although we do sometimes throw in other examples). We’ll build up
this project as the chapters progress, as if you’ve paired with us and
we’re explaining what we’re doing and why at each step.
But to really get to grips with these patterns, you need to mess about
```
[^25]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 10 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.32)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.32, lines 18–23)*:
```
well ordered, but over time we find that it gathers cruft and edge cases
and ends up a confusing morass of manager classes and util modules.
We find that our sensibly layered architecture has collapsed into itself
like an oversoggy trifle. Chaotic software systems are characterized by
a sameness of function: API handlers that have domain knowledge and
send email and perform logging; “business logic” classes that perform
```
[^26]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.34)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.34, lines 11–18)*:
```
background theme of the book.
The term encapsulation covers two closely related ideas: simplifying
behavior and hiding data. In this discussion, we’re using the first
sense. We encapsulate behavior by identifying a task that needs to be
done in our code and giving that task to a well-defined object or
function. We call that object or function an abstraction.
Take a look at the following two snippets of Python code:
Do a search with urllib
```
[^27]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.45)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.45, lines 5–9)*:
```
the Flask API, the ORM, and Postgres—for a totally different
I/O model involving a CLI and CSVs.
Finally, Appendix D may be of interest if you’re wondering
how these patterns might look if using Django instead of Flask
and SQLAlchemy.
```
[^28]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.32)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.32, lines 9–16)*:
```
For example, a well-tended garden is a highly ordered system.
Gardeners define boundaries with paths and fences, and they mark out
flower beds or vegetable patches. Over time, the garden evolves,
growing richer and thicker; but without deliberate effort, the garden
will run wild. Weeds and grasses will choke out other plants, covering
over the paths, until eventually every part looks the same again—wild
and unmanaged.
Software systems, too, tend toward chaos. When we first start building
```
[^29]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Duck Typing** *(p.36)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.36, lines 10–17)*:
```
interface to define an abstraction. In Python you can (and we sometimes do) use ABCs, but you
can also happily rely on duck typing.
The abstraction can just mean “the public API of the thing you’re using”—a function name plus
some arguments, for example.
Most of the patterns in this book involve choosing an abstraction, so
you’ll see plenty of examples in each chapter. In addition, Chapter 3
specifically discusses some general heuristics for choosing
abstractions.
```
[^30]
**Annotation:** This excerpt demonstrates 'duck typing' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.33)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.33, lines 1–6)*:
```
no calculations but do perform I/O; and everything coupled to
everything else so that changing any part of the system becomes fraught
with danger. This is so common that software engineers have their own
term for chaos: the Big Ball of Mud anti-pattern (Figure P-1).
Figure P-1. A real-life dependency diagram (source: “Enterprise Dependency: Big Ball
of Yarn” by Alex Papadimoulis)
```
[^31]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Encapsulation** *(p.34)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.34, lines 6–13)*:
```
complex.
Encapsulation and Abstractions
Encapsulation and abstraction are tools that we all instinctively reach
for as programmers, even if we don’t all use these exact words. Allow
us to dwell on them for a moment, since they are a recurring
background theme of the book.
The term encapsulation covers two closely related ideas: simplifying
behavior and hiding data. In this discussion, we’re using the first
```
[^32]
**Annotation:** This excerpt demonstrates 'encapsulation' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.28)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.28, lines 2–9)*:
```
Italic
Indicates new terms, URLs, email addresses, filenames, and file
extensions.
Constant width
Used for program listings, as well as within paragraphs to refer to
program elements such as variable or function names, databases,
data types, environment variables, statements, and keywords.
Constant width bold
```
[^33]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.25)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.25, lines 8–15)*:
```
discuss how events can be used as a pattern for integration
between services in a microservices architecture. Finally, we
distinguish between commands and events. Our application is now
fundamentally a message-processing system.
Command-query responsibility segregation (Chapter 12)
We present an example of command-query responsibility
segregation, with and without events.
Dependency injection (Chapter 13)
```
[^34]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.25)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.25, lines 18–25)*:
```
Addtional Content
How do I get there from here? (Epilogue)
Implementing architectural patterns always looks easy when you
show a simple example, starting from scratch, but many of you will
probably be wondering how to apply these principles to existing
software. We’ll provide a few pointers in the epilogue and some
links to further reading.
Example Code and Coding Along
```
[^35]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 3: A Brief Interlude: On Coupling and Abstractions** *(pp.47–58)*

This later chapter builds upon the concepts introduced here, particularly: None, argument, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^36]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, argument appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Our First Use Case: Flask API and Service Layer** *(pp.59–86)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^37]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: TDD in High Gear and Low Gear** *(pp.87–104)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^38]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 3: A Brief Interlude: On Coupling and Abstractions

*Source: Architecture Patterns with Python, pages 47–58*

### Chapter Summary
Discusses software coupling and abstractions as fundamental architectural concepts. Examines the tradeoffs between loose and tight coupling, dependency inversion principle, and designing clean interfaces and boundaries. [^39]

### Concept-by-Concept Breakdown
#### **None** *(p.57)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.57, lines 24–31)*:
```
def test_cannot_allocate_if_skus_do_not_match(): 
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None) 
    different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10) 
    assert batch.can_allocate(different_sku_line) is False
There’s nothing too unexpected here. We’ve refactored our test suite so
that we don’t keep repeating the same lines of code to create a batch
and a line for the same SKU; and we’ve written four simple tests for a
new method can_allocate. Again, notice that the names we use
```
[^40]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.56)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.56, lines 7–14)*:
```
class Batch:
    def __init__(
        self, ref: str, sku: str, qty: int, eta: Optional[date]  
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty
```
[^41]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.56)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.56, lines 25–31)*:
```
For domain models, they can sometimes help to clarify or
document what the expected arguments are, and people with IDEs
are often grateful for them. You may decide the price paid in terms
of readability is too high.
Our implementation here is trivial: a Batch just wraps an integer
available_quantity, and we decrement that value on allocation.
2
```
[^42]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.54)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.54, lines 2–9)*:
```
ubiquitous language in DDD terminology). We choose memorable
identifiers for our objects so that the examples are easier to talk about.
“Some Notes on Allocation” shows some notes we might have taken
while having a conversation with our domain experts about allocation.
SOME NOTES ON ALLOCATION
A product is identified by a SKU, pronounced “skew,” which is short for stock-keeping unit.
Customers place orders. An order is identified by an order reference and comprises multiple
order lines, where each line has a SKU and a quantity. For example:
```
[^43]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.57)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.57, lines 13–20)*:
```
    large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2) 
    assert large_batch.can_allocate(small_line) 
 
def test_cannot_allocate_if_available_smaller_than_required(): 
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20) 
    assert small_batch.can_allocate(large_line) is False 
 
def test_can_allocate_if_available_equal_to_required(): 
```
[^44]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.56)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.56, lines 1–8)*:
```
First cut of a domain model for batches (model.py)
@dataclass(frozen=True)  
class OrderLine:
    orderid: str
    sku: str
    qty: int
class Batch:
    def __init__(
```
[^45]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Datetime** *(p.56)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.56, lines 20–27)*:
```
from dataclasses import dataclass; likewise,
typing.Optional and datetime.date. If you want to double-
check anything, you can see the full working code for each chapter
in its branch (e.g., chapter_01_domain_model).
Type hints are still a matter of controversy in the Python world.
For domain models, they can sometimes help to clarify or
document what the expected arguments are, and people with IDEs
are often grateful for them. You may decide the price paid in terms
```
[^46]
**Annotation:** This excerpt demonstrates 'datetime' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.57)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.57, lines 4–11)*:
```
Testing logic for what we can allocate (test_batches.py)
def make_batch_and_line(sku, batch_qty, line_qty): 
    return ( 
        Batch("batch-001", sku, batch_qty, eta=date.today()), 
        OrderLine("order-123", sku, line_qty) 
    ) 
 
 
```
[^47]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.48)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.48, lines 15–22)*:
```
A model is a map of a process or phenomenon that captures a useful
property. Humans are exceptionally good at producing models of
things in their heads. For example, when someone throws a ball
toward you, you’re able to predict its movement almost unconsciously,
because you have a model of the way objects move in space. Your
model isn’t perfect by any means. Humans have terrible intuitions
about how objects behave at near-light speeds or in a vacuum because
our model was never designed to cover those cases. That doesn’t mean
```
[^48]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.48)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.48, lines 15–22)*:
```
A model is a map of a process or phenomenon that captures a useful
property. Humans are exceptionally good at producing models of
things in their heads. For example, when someone throws a ball
toward you, you’re able to predict its movement almost unconsciously,
because you have a model of the way objects move in space. Your
model isn’t perfect by any means. Humans have terrible intuitions
about how objects behave at near-light speeds or in a vacuum because
our model was never designed to cover those cases. That doesn’t mean
```
[^49]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.55)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.55, lines 2–9)*:
```
We’re not going to show you how TDD works in this book, but we
want to show you how we would construct a model from this business
conversation.
EXERCISE FOR THE READER
Why not have a go at solving this problem yourself? Write a few unit tests to see if you can
capture the essence of these business rules in nice, clean code.
You’ll find some placeholder unit tests on GitHub, but you could just start from scratch, or
combine/rewrite them however you like.
```
[^50]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.49)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.49, lines 15–20)*:
```
Within a couple of weeks, you’d become more precise as you adopted
words to describe the ship’s functions: “Increase oxygen levels in
cargo bay three” or “turn on the little thrusters.” After a few months,
you’d have adopted language for entire complex processes: “Start
landing sequence” or “prepare for warp.” This process would happen
quite naturally, without any formal effort to build a shared glossary.
```
[^51]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Immutable** *(p.56)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.56, lines 16–23)*:
```
        self.available_quantity -= line.qty  
OrderLine is an immutable dataclass with no behavior.
We’re not showing imports in most code listings, in an attempt to
keep them clean. We’re hoping you can guess that this came via
from dataclasses import dataclass; likewise,
typing.Optional and datetime.date. If you want to double-
check anything, you can see the full working code for each chapter
in its branch (e.g., chapter_01_domain_model).
```
[^52]
**Annotation:** This excerpt demonstrates 'immutable' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.56)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.56, lines 17–24)*:
```
OrderLine is an immutable dataclass with no behavior.
We’re not showing imports in most code listings, in an attempt to
keep them clean. We’re hoping you can guess that this came via
from dataclasses import dataclass; likewise,
typing.Optional and datetime.date. If you want to double-
check anything, you can see the full working code for each chapter
in its branch (e.g., chapter_01_domain_model).
Type hints are still a matter of controversy in the Python world.
```
[^53]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Integer** *(p.56)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.56, lines 28–31)*:
```
of readability is too high.
Our implementation here is trivial: a Batch just wraps an integer
available_quantity, and we decrement that value on allocation.
2
```
[^54]
**Annotation:** This excerpt demonstrates 'integer' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 4: Our First Use Case: Flask API and Service Layer** *(pp.59–86)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^55]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: TDD in High Gear and Low Gear** *(pp.87–104)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^56]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Unit of Work Pattern** *(pp.105–132)*

This later chapter builds upon the concepts introduced here, particularly: None, argument, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^57]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, argument appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 4: Our First Use Case: Flask API and Service Layer

*Source: Architecture Patterns with Python, pages 59–86*

### Chapter Summary
Demonstrates building a Flask API with a service layer to orchestrate use cases. Shows how to separate API concerns from business logic, implement application services, and structure REST endpoints properly. [^58]

### Concept-by-Concept Breakdown
#### **Gil** *(p.76)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.76, lines 18–23)*:
```
external state.
We expect to be working in an agile manner, so our priority is to get to
a minimum viable product as quickly as possible. In our case, that’s
going to be a web API. In a real project, you might dive straight in
with some end-to-end tests and start plugging in a web framework,
test-driving things outside-in.
```
[^59]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.69)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.69, lines 5–12)*:
```
    def __gt__(self, other): 
        if self.eta is None: 
            return False 
        if other.eta is None: 
            return True 
        return self.eta > other.eta
That’s lovely.
Exceptions Can Express Domain Concepts Too
```
[^60]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Eq__** *(p.66)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.66, lines 2–9)*:
```
        return hash(self.reference)
Python’s __eq__ magic method defines the behavior of the class for
the == operator.
For both entity and value objects, it’s also worth thinking through how
__hash__ will work. It’s the magic method Python uses to control the
behavior of objects when you add them to sets or use them as dict
keys; you can find more info in the Python docs.
For value objects, the hash should be based on all the value attributes,
```
[^61]
**Annotation:** This excerpt demonstrates '__eq__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.61)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.61, lines 18–25)*:
```
class Batch: 
    def __init__(self, ref: Reference, sku: Sku, qty: Quantity): 
        self.sku = sku 
        self.reference = ref 
        self._purchased_quantity = qty
That would allow our type checker to make sure that we don’t pass a Sku where a Reference is
expected, for example.
Whether you think this is wonderful or appalling is a matter of debate.
```
[^62]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.74)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.74, lines 4–11)*:
```
concerns.
We’ll introduce the Repository pattern, a simplifying abstraction over
data storage, allowing us to decouple our model layer from the data
layer. We’ll present a concrete example of how this simplifying
abstraction makes our system more testable by hiding the complexities
of the database.
Figure 2-1 shows a little preview of what we’re going to build: a
Repository object that sits between our domain model and the
```
[^63]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.85)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.85, lines 20–27)*:
```
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]
If you haven’t used pytest, the session argument to this test needs
explaining. You don’t need to worry about the details of pytest or
its fixtures for the purposes of this book, but the short explanation
is that you can define common dependencies for your tests as
“fixtures,” and pytest will inject them to the tests that need them by
looking at their function arguments. In this case, it’s a SQLAlchemy
database session.
```
[^64]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.66)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.66, lines 1–8)*:
```
def __hash__(self): 
        return hash(self.reference)
Python’s __eq__ magic method defines the behavior of the class for
the == operator.
For both entity and value objects, it’s also worth thinking through how
__hash__ will work. It’s the magic method Python uses to control the
behavior of objects when you add them to sets or use them as dict
keys; you can find more info in the Python docs.
```
[^65]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 16 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.63)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.63, lines 12–19)*:
```
def test_equality(): 
    assert Money('gbp', 10) == Money('gbp', 10) 
    assert Name('Harry', 'Percival') != Name('Bob', 'Gregory') 
    assert Line('RED-CHAIR', 5) == Line('RED-CHAIR', 5)
These value objects match our real-world intuition about how their
values work. It doesn’t matter which £10 note we’re talking about,
because they all have the same value. Likewise, two names are equal
if both the first and last names match; and two lines are equivalent if
```
[^66]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.66)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.66, lines 8–15)*:
```
keys; you can find more info in the Python docs.
For value objects, the hash should be based on all the value attributes,
and we should ensure that the objects are immutable. We get this for
free by specifying @frozen=True on the dataclass.
For entities, the simplest option is to say that the hash is None, meaning
that the object is not hashable and cannot, for example, be used in a
set. If for some reason you decide you really do want to use set or dict
operations with entities, the hash should be based on the attribute(s),
```
[^67]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.83)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.83, lines 5–12)*:
```
Django ORM example
class Order(models.Model): 
    pass 
 
class OrderLine(models.Model): 
    sku = models.CharField(max_length=255) 
    qty = models.IntegerField() 
    order = models.ForeignKey(Order) 
```
[^68]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.70)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.70, lines 2–9)*:
```
Domain modeling
This is the part of your code that is closest to the business, the most likely to change, and the
place where you deliver the most value to the business. Make it easy to understand and
modify.
Distinguish entities from value objects
A value object is defined by its attributes. It’s usually best implemented as an immutable
type. If you change an attribute on a Value Object, it represents a different object. In contrast,
an entity has attributes that may vary over time and it will still be the same entity. It’s important
```
[^69]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.62)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.62, lines 27–28)*:
```
from typing import NamedTuple
from collections import namedtuple
```
[^70]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.64)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.64, lines 25–26)*:
```
But what about Harry as a person? People do change their names, and
their marital status, and even their gender, but we continue to recognize
```
[^71]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.59)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.59, lines 5–12)*:
```
 
    def allocate(self, line: OrderLine): 
        if self.can_allocate(line): 
            self._allocations.add(line) 
 
    def deallocate(self, line: OrderLine): 
        if line in self._allocations: 
            self._allocations.remove(line) 
```
[^72]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Encapsulation** *(p.61)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.61, lines 4–11)*:
```
and spreadsheets. We’ll see how sticking rigidly to our principles of
encapsulation and careful layering will help us to avoid a ball of mud.
MORE TYPES FOR MORE TYPE HINTS
If you really want to go to town with type hints, you could go so far as wrapping primitive types by
using typing.NewType:
Just taking it way too far, Bob
from dataclasses import dataclass
from typing import NewType 
```
[^73]
**Annotation:** This excerpt demonstrates 'encapsulation' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 5: TDD in High Gear and Low Gear** *(pp.87–104)*

This later chapter builds upon the concepts introduced here, particularly: None, __eq__, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^74]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __eq__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Unit of Work Pattern** *(pp.105–132)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^75]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Aggregates and Consistency Boundaries** *(pp.133–154)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^76]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 5: TDD in High Gear and Low Gear

*Source: Architecture Patterns with Python, pages 87–104*

### Chapter Summary
Explores test-driven development practices at different levels (high gear vs low gear). Covers the test pyramid, balancing unit tests vs integration tests, and using pytest effectively with mocks and fixtures. [^77]

### Concept-by-Concept Breakdown
#### **None** *(p.91)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.91, lines 2–9)*:
```
def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)
    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)  
    session.commit()  
    rows = list(session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'  
    ))
```
[^78]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Eq__** *(p.92)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.92, lines 10–17)*:
```
    expected = model.Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected  # Batch.__eq__ only compares reference  
    assert retrieved.sku == expected.sku  
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {  
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }
This tests the read side, so the raw SQL is preparing data to be
```
[^79]
**Annotation:** This excerpt demonstrates '__eq__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.93)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.93, lines 8–15)*:
```
 
    def __init__(self, session): 
        self.session = session 
 
    def add(self, batch): 
        self.session.add(batch) 
 
    def get(self, reference): 
```
[^80]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.103)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.103, lines 2–9)*:
```
On Coupling and
Abstractions
Allow us a brief digression on the subject of abstractions, dear reader.
We’ve talked about abstractions quite a lot. The Repository pattern is
an abstraction over permanent storage, for example. But what makes a
good abstraction? What do we want from abstractions? And how do
they relate to testing?
TIP
```
[^81]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.96)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.96, lines 2–9)*:
```
duck type that your adapters conform to and that your core application
expects—the function and method names in use, and their argument
names and types.
Concretely, in this chapter, AbstractRepository is the port, and
SqlAlchemyRepository and FakeRepository are the adapters.
Wrap-Up
Bearing the Rich Hickey quote in mind, in each chapter we summarize
the costs and benefits of each architectural pattern we introduce. We
```
[^82]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.89)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.89, lines 1–8)*:
```
ABSTRACT BASE CLASSES, DUCK TYPING, AND PROTOCOLS
We’re using abstract base classes in this book for didactic reasons: we hope they help explain
what the interface of the repository abstraction is.
In real life, we’ve sometimes found ourselves deleting ABCs from our production code, because
Python makes it too easy to ignore them, and they end up unmaintained and, at worst,
misleading. In practice we often just rely on Python’s duck typing to enable abstractions. To a
Pythonista, a repository is any object that has add(thing) and get(id) methods.
An alternative to look into is PEP 544 protocols. These give you typing without the possibility of
```
[^83]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 13 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.92)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.92, lines 10–17)*:
```
    expected = model.Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected  # Batch.__eq__ only compares reference  
    assert retrieved.sku == expected.sku  
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {  
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }
This tests the read side, so the raw SQL is preparing data to be
```
[^84]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.90)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.90, lines 14–19)*:
```
is correctly integrated with the database; hence, the tests tend to mix
raw SQL with calls and assertions on our own code.
TIP
Unlike the ORM tests from earlier, these tests are good candidates for staying
part of your codebase longer term, particularly if any parts of your domain model
mean the object-relational map is nontrivial.
```
[^85]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.92)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.92, lines 25–30)*:
```
remember, Batch is an entity, and we have a custom eq for it).
So we also explicitly check on its major attributes, including
._allocations, which is a Python set of OrderLine value
objects.
Whether or not you painstakingly write tests for every model is a
judgment call. Once you have one class tested for create/modify/save,
```
[^86]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.104)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.104, lines 1–8)*:
```
When we’re unable to change component A for fear of breaking
component B, we say that the components have become coupled.
Locally, coupling is a good thing: it’s a sign that our code is working
together, each component supporting the others, all of them fitting in
place like the gears of a watch. In jargon, we say this works when
there is high cohesion between the coupled elements.
Globally, coupling is a nuisance: it increases the risk and the cost of
changing our code, sometimes to the point where we feel unable to
```
[^87]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.88)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.88, lines 8–15)*:
```
our domain model to the database.
Here’s what an abstract base class (ABC) for our repository would
look like:
The simplest possible repository (repository.py)
class AbstractRepository(abc.ABC):
    @abc.abstractmethod  
    def add(self, batch: model.Batch):
        raise NotImplementedError  
```
[^88]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.93)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.93, lines 8–15)*:
```
 
    def __init__(self, session): 
        self.session = session 
 
    def add(self, batch): 
        self.session.add(batch) 
 
    def get(self, reference): 
```
[^89]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Duck Typing** *(p.89)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.89, lines 1–8)*:
```
ABSTRACT BASE CLASSES, DUCK TYPING, AND PROTOCOLS
We’re using abstract base classes in this book for didactic reasons: we hope they help explain
what the interface of the repository abstraction is.
In real life, we’ve sometimes found ourselves deleting ABCs from our production code, because
Python makes it too easy to ignore them, and they end up unmaintained and, at worst,
misleading. In practice we often just rely on Python’s duck typing to enable abstractions. To a
Pythonista, a repository is any object that has add(thing) and get(id) methods.
An alternative to look into is PEP 544 protocols. These give you typing without the possibility of
```
[^90]
**Annotation:** This excerpt demonstrates 'duck typing' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.103)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.103, lines 16–19)*:
```
things out and refactoring aggressively. In a large-scale system, though,
we become constrained by the decisions made elsewhere in the
system.
1
```
[^91]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.101)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.101, lines 25–27)*:
```
world, we modify our model objects one at a time, and delete is usually handled as a soft-
delete—i.e., batch.cancel(). Finally, update is taken care of by the Unit of Work
pattern, as you’ll see in Chapter 6.
```
[^92]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 6: Unit of Work Pattern** *(pp.105–132)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^93]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Aggregates and Consistency Boundaries** *(pp.133–154)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^94]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Events and the Message Bus** *(pp.155–188)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^95]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 6: Unit of Work Pattern

*Source: Architecture Patterns with Python, pages 105–132*

### Chapter Summary
Introduces the Unit of Work pattern for managing database transactions and ensuring atomic operations. Covers transaction boundaries, commit/rollback semantics, session management, and implementing UoW as a context manager. [^96]

### Concept-by-Concept Breakdown
#### **Gil** *(p.126)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.126, lines 13–20)*:
```
World
Like any good agile team, we’re hustling to try to get an MVP out and
in front of the users to start gathering feedback. We have the core of
our domain model and the domain service we need to allocate orders,
and we have the repository interface for permanent storage.
Let’s plug all the moving parts together as quickly as we can and then
refactor toward a cleaner architecture. Here’s our plan:
1. Use Flask to put an API endpoint in front of our allocate
```
[^97]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.128)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.128, lines 3–10)*:
```
        (earlybatch, sku, 100, '2011-01-01'),
        (otherbatch, othersku, 100, None),
    ])
    data = {'orderid': random_orderid(), 'sku': sku, 'qty': 3}
    url = config.get_api_url()  
    r = requests.post(f'{url}/allocate', json=data)
    assert r.status_code == 201
    assert r.json()['batchref'] == earlybatch
```
[^98]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.129)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.129, lines 12–19)*:
```
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__) 
 
@app.route("/allocate", methods=['POST'])
def allocate_endpoint(): 
    session = get_session() 
    batches = repository.SqlAlchemyRepository(session).list() 
    line = model.OrderLine( 
```
[^99]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.105)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.105, lines 4–11)*:
```
In Figure 3-2, though, we have reduced the degree of coupling by
inserting a new, simpler abstraction. Because it is simpler, system A
has fewer kinds of dependencies on the abstraction. The abstraction
serves to protect us from change by hiding away the complex details of
whatever system B does—we can change the arrows on the right
without changing the ones on the left.
Abstracting State Aids Testability
Let’s see an example. Imagine we want to write code for synchronizing
```
[^100]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.118)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.118, lines 19–24)*:
```
tests verify the interactions between things: did we call
shutil.copy with the right arguments? This coupling
between code and test tends to make tests more brittle, in our
experience.
Overuse of mocks leads to complicated test suites that fail to
explain the code.
```
[^101]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.107)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.107, lines 2–9)*:
```
 
    # Walk the target folder and get the filenames and hashes 
    for folder, _, files in os.walk(dest): 
        for fn in files: 
            dest_path = Path(folder) / fn 
            dest_hash = hash_file(dest_path) 
            seen.add(dest_hash) 
 
```
[^102]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 17 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.108)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.108, lines 1–8)*:
```
expected_path = Path(dest) /  'my-file' 
        assert expected_path.exists() 
        assert expected_path.read_text() == content 
 
    finally: 
        shutil.rmtree(source) 
        shutil.rmtree(dest) 
 
```
[^103]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.119)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.119, lines 10–17)*:
```
for use only in tests. They wouldn’t work “in real life”; our in-memory repository is a
good example. But you can use them to make assertions about the end state of a
system rather than the behaviors along the way, so they’re associated with classic-style
TDD.
We’re slightly conflating mocks with spies and fakes with stubs here, and you can read the long,
correct answer in Martin Fowler’s classic essay on the subject called “Mocks Aren’t Stubs”.
It also probably doesn’t help that the MagicMock objects provided by unittest.mock aren’t, strictly
speaking, mocks; they’re spies, if anything. But they’re also often used as stubs or dummies.
```
[^104]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.119)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.119, lines 3–10)*:
```
little more complexity for a cleaner design that admits novel use cases.
MOCKS VERSUS FAKES; CLASSIC-STYLE VERSUS LONDON-
SCHOOL TDD
Here’s a short and somewhat simplistic definition of the difference between mocks and fakes:
Mocks are used to verify how something gets used; they have methods like
assert_called_once_with(). They’re associated with London-school TDD.
Fakes are working implementations of the thing they’re replacing, but they’re designed
for use only in tests. They wouldn’t work “in real life”; our in-memory repository is a
```
[^105]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.118)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.118, lines 10–17)*:
```
injection in Chapter 13.
We have three closely related reasons for our preference:
Patching out the dependency you’re using makes it possible to
unit test the code, but it does nothing to improve the design.
Using mock.patch won’t let your code work with a --dry-
run flag, nor will it help you run against an FTP server. For
that, you’ll need to introduce abstractions.
Tests that use mocks tend to be more coupled to the
```
[^106]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.116)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.116, lines 5–12)*:
```
TIP
Although we’re using dependency injection, there is no need to define an abstract
base class or any kind of explicit interface. In this book, we often show ABCs
because we hope they help you understand what the abstraction is, but they’re not
necessary. Python’s dynamic nature means we can always rely on duck typing.
Tests using DI
class FakeFileSystem(list): 
    def copy(self, src, dest): 
```
[^107]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Dictionary** *(p.110)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.110, lines 13–20)*:
```
For steps 1 and 2, we’ve already intuitively started using an
abstraction, a dictionary of hashes to paths. You may already have
been thinking, “Why not build up a dictionary for the destination folder
as well as the source, and then we just compare two dicts?” That
seems like a nice way to abstract the current state of the filesystem:
source_files = {'hash1': 'path1', 'hash2': 'path2'} 
dest_files = {'hash1': 'path1', 'hash2': 'pathX'}
What about moving from step 2 to step 3? How can we abstract out the
```
[^108]
**Annotation:** This excerpt demonstrates 'dictionary' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Duck Typing** *(p.116)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.116, lines 8–15)*:
```
because we hope they help you understand what the abstraction is, but they’re not
necessary. Python’s dynamic nature means we can always rely on duck typing.
Tests using DI
class FakeFileSystem(list): 
    def copy(self, src, dest): 
        self.append(('COPY', src, dest))
    def move(self, src, dest):
        self.append(('MOVE', src, dest))
```
[^109]
**Annotation:** This excerpt demonstrates 'duck typing' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Elif** *(p.107)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.107, lines 15–22)*:
```
            # move it to the correct path 
            elif dest_hash in source_hashes and fn != source_hashes[dest_hash]: 
                shutil.move(dest_path, Path(folder) / source_hashes[dest_hash]) 
 
    # for every file that appears in source but not target, copy the file to 
    # the target 
    for src_hash, fn in source_hashes.items(): 
        if src_hash not in seen: 
```
[^110]
**Annotation:** This excerpt demonstrates 'elif' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Error Handling** *(p.130)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.130, lines 27–31)*:
```
uglier.
Suppose we want to add a bit of error handling. What if the domain
raises an error, for a SKU that’s out of stock? Or what about a SKU
that doesn’t even exist? That’s not something the domain even knows
about, nor should it. It’s more of a sanity check that we should
```
[^111]
**Annotation:** This excerpt demonstrates 'error handling' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 7: Aggregates and Consistency Boundaries** *(pp.133–154)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^112]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Events and the Message Bus** *(pp.155–188)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^113]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Going to Town on the Message Bus** *(pp.189–214)*

This later chapter builds upon the concepts introduced here, particularly: None, as, assert.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^114]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 7: Aggregates and Consistency Boundaries

*Source: Architecture Patterns with Python, pages 133–154*

### Chapter Summary
Examines aggregates as consistency boundaries in domain-driven design. Discusses aggregate roots, enforcing invariants, transactional boundaries, and designing for consistency vs eventual consistency in distributed systems. [^115]

### Concept-by-Concept Breakdown
#### **None** *(p.134)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.134, lines 2–9)*:
```
    line = model.OrderLine("o1", "COMPLICATED-LAMP", 10)
    batch = model.Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
    repo = FakeRepository([batch])  
    result = services.allocate(line, repo, FakeSession())  
    assert result == "b1"
def test_error_for_invalid_sku():
    line = model.OrderLine("o1", "NONEXISTENTSKU", 10)
    batch = model.Batch("b1", "AREALSKU", 100, eta=None)
```
[^116]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.141)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.141, lines 1–8)*:
```
├── service_layer   
│   ├── __init__.py 
│   └── services.py 
├── adapters   
│   ├── __init__.py 
│   ├── orm.py 
│   └── repository.py 
├── entrypoints   
```
[^117]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.136)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.136, lines 7–14)*:
```
Chapter 6 with the Unit of Work pattern.
DEPEND ON ABSTRACTIONS
Notice one more thing about our service-layer function:
def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
It depends on a repository. We’ve chosen to make the dependency explicit, and we’ve used the
type hint to say that we depend on AbstractRepository. This means it’ll work both when the tests
give it a FakeRepository and when the Flask app gives it a SqlAlchemyRepository.
If you remember “The Dependency Inversion Principle”, this is what we mean when we say we
```
[^118]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.142)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.142, lines 2–9)*:
```
official ports and adapters terminology, these are adapters too, and
are referred to as primary, driving, or outward-facing adapters.
What about ports? As you may remember, they are the abstract
interfaces that the adapters implement. We tend to keep them in the
same file as the adapters that implement them.
Wrap-Up
Adding the service layer has really bought us quite a lot:
Our Flask API endpoints become very thin and easy to write:
```
[^119]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 14 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.138)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.138, lines 8–15)*:
```
    r = requests.post(f'{url}/allocate', json=data) 
    assert r.status_code == 201 
    assert r.json()['batchref'] == earlybatch 
 
 
@pytest.mark.usefixtures('restart_api')
def test_unhappy_path_returns_400_and_error_message(): 
    unknown_sku, orderid = random_sku(), random_orderid() 
```
[^120]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.136)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.136, lines 1–8)*:
```
We make some checks or assertions about the request against the
current state of the world.
We call a domain service.
If all is well, we save/update any state we’ve changed.
That last step is a little unsatisfactory at the moment, as our service
layer is tightly coupled to our database layer. We’ll improve that in
Chapter 6 with the Unit of Work pattern.
DEPEND ON ABSTRACTIONS
```
[^121]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.153)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.153, lines 6–13)*:
```
only against the service layer, we won’t have any tests that directly
interact with “private” methods or attributes on our model objects,
which leaves us freer to refactor them.
TIP
Every line of code that we put in a test is like a blob of glue, holding the system in
a particular shape. The more low-level tests we have, the harder it will be to
change things.
On Deciding What Kind of Tests to Write
```
[^122]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.152)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.152, lines 31–33)*:
```
and that orders are still being allocated.
If we accidentally change one of those behaviors, our tests will break.
The flip side, though, is that if we want to change the design of our
```
[^123]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.141)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.141, lines 24–31)*:
```
file, but for a more complex application, you might have one file
per class; you might have helper parent classes for Entity,
ValueObject, and Aggregate, and you might add an
exceptions.py for domain-layer exceptions and, as you’ll see in
Part II, commands.py and events.py.
We’ll distinguish the service layer. Currently that’s just one file
called services.py for our service-layer functions. You could add
service-layer exceptions here, and as you’ll see in Chapter 5,
```
[^124]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.149)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.149, lines 7–12)*:
```
Chapter 6, we’ll introduce one more pattern that works
closely with the Repository and Service Layer patterns, the
Unit of Work pattern, and everything will be absolutely
lovely. You’ll see!
1  Service-layer services and domain services do have confusingly similar names. We
tackle this topic later in “Why Is Everything Called a Service?”.
```
[^125]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.152)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.152, lines 29–33)*:
```
change while we’re working. We use tests to check that the API
continues to return 200, that the database session continues to commit,
and that orders are still being allocated.
If we accidentally change one of those behaviors, our tests will break.
The flip side, though, is that if we want to change the design of our
```
[^126]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.133)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.133, lines 13–20)*:
```
 
    def __init__(self, batches): 
        self._batches = set(batches) 
 
    def add(self, batch): 
        self._batches.add(batch) 
 
    def get(self, reference): 
```
[^127]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.141)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.141, lines 26–33)*:
```
ValueObject, and Aggregate, and you might add an
exceptions.py for domain-layer exceptions and, as you’ll see in
Part II, commands.py and events.py.
We’ll distinguish the service layer. Currently that’s just one file
called services.py for our service-layer functions. You could add
service-layer exceptions here, and as you’ll see in Chapter 5,
we’ll add unit_of_work.py.
Adapters is a nod to the ports and adapters terminology. This will
```
[^128]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.141)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.141, lines 26–33)*:
```
ValueObject, and Aggregate, and you might add an
exceptions.py for domain-layer exceptions and, as you’ll see in
Part II, commands.py and events.py.
We’ll distinguish the service layer. Currently that’s just one file
called services.py for our service-layer functions. You could add
service-layer exceptions here, and as you’ll see in Chapter 5,
we’ll add unit_of_work.py.
Adapters is a nod to the ports and adapters terminology. This will
```
[^129]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.141)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.141, lines 23–30)*:
```
Let’s have a folder for our domain model. Currently that’s just one
file, but for a more complex application, you might have one file
per class; you might have helper parent classes for Entity,
ValueObject, and Aggregate, and you might add an
exceptions.py for domain-layer exceptions and, as you’ll see in
Part II, commands.py and events.py.
We’ll distinguish the service layer. Currently that’s just one file
called services.py for our service-layer functions. You could add
```
[^130]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 8: Events and the Message Bus** *(pp.155–188)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^131]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Going to Town on the Message Bus** *(pp.189–214)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^132]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: Commands and Command Handler** *(pp.215–234)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^133]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 8: Events and the Message Bus

*Source: Architecture Patterns with Python, pages 155–188*

### Chapter Summary
Introduces domain events and the message bus pattern for decoupling components. Covers event publishing and subscribing, implementing an event-driven architecture, and using events to communicate domain state changes asynchronously. [^134]

### Concept-by-Concept Breakdown
#### **None** *(p.160)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.160, lines 1–8)*:
```
repo, session = FakeRepository([]), FakeSession() 
    services.add_batch("b1", "AREALSKU", 100, None, repo, session) 
 
    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"): 
        services.allocate("o1", "NONEXISTENTSKU", 10, repo, FakeSession())
This is a really nice place to be in. Our service-layer tests depend on
only the service layer itself, leaving us completely free to refactor the
model as we see fit.
```
[^135]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.172)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.172, lines 6–13)*:
```
        self.session_factory = session_factory  
    def __enter__(self):
        self.session = self.session_factory()  # type: Session  
        self.batches = repository.SqlAlchemyRepository(self.session)  
        return super().__enter__()
    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()  
```
[^136]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.171)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.171, lines 1–8)*:
```
def __exit__(self, *args):  
        self.rollback()  
    @abc.abstractmethod
    def commit(self):  
        raise NotImplementedError
    @abc.abstractmethod
    def rollback(self):  
        raise NotImplementedError
```
[^137]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.172)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.172, lines 4–11)*:
```
class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory  
    def __enter__(self):
        self.session = self.session_factory()  # type: Session  
        self.batches = repository.SqlAlchemyRepository(self.session)  
        return super().__enter__()
    def __exit__(self, *args):
```
[^138]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.183)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.183, lines 8–15)*:
```
UNIT OF WORK PATTERN RECAP
The Unit of Work pattern is an abstraction around data integrity
It helps to enforce the consistency of our domain model, and improves performance, by
letting us perform a single flush operation at the end of an operation.
It works closely with the Repository and Service Layer patterns
The Unit of Work pattern completes our abstractions over data access by representing
atomic updates. Each of our service-layer use cases runs in a single unit of work that
succeeds or fails as a block.
```
[^139]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.172)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.172, lines 10–17)*:
```
        return super().__enter__()
    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()  
    def commit(self):  
        self.session.commit()
    def rollback(self):  
        self.session.rollback()
```
[^140]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.180)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.180, lines 5–12)*:
```
test_repository.py. That last test, you might keep around, but we could
certainly see an argument for just keeping everything at the highest
possible level of abstraction (just as we did for the unit tests).
EXERCISE FOR THE READER
For this chapter, probably the best thing to try is to implement a UoW from scratch. The code, as
always, is on GitHub. You could either follow the model we have quite closely, or perhaps
experiment with separating the UoW (whose responsibilities are commit(), rollback(), and
providing the .batches repository) from the context manager, whose job is to initialize things, and
```
[^141]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.174)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.174, lines 1–8)*:
```
In our tests, we can instantiate a UoW and pass it to our service
layer, rather than passing a repository and a session. This is
considerably less cumbersome.
DON’T MOCK WHAT YOU DON’T OWN
Why do we feel more comfortable mocking the UoW than the session? Both of our fakes achieve
the same thing: they give us a way to swap out our persistence layer so we can run tests in
memory instead of needing to talk to a real database. The difference is in the resulting design.
If we cared only about writing tests that run quickly, we could create mocks that replace
```
[^142]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 10 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.158)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.158, lines 7–14)*:
```
FakeSession()) 
    assert result == "batch1"
At least that would move all of our tests’ dependencies on the domain
into one place.
Adding a Missing Service
We could go one step further, though. If we had a service to add stock,
we could use that and make our service-layer tests fully expressed in
terms of the service layer’s official use cases, removing all
```
[^143]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.171)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.171, lines 8–15)*:
```
        raise NotImplementedError
The UoW provides an attribute called .batches, which will give
us access to the batches repository.
If you’ve never seen a context manager, __enter__ and __exit__
are the two magic methods that execute when we enter the with
block and when we exit it, respectively. They’re our setup and
teardown phases.
We’ll call this method to explicitly commit our work when we’re
```
[^144]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.176)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.176, lines 1–8)*:
```
def test_rolls_back_on_error(session_factory): 
    class MyException(Exception): 
        pass 
 
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory) 
    with pytest.raises(MyException): 
        with uow: 
            insert_batch(uow.session, 'batch1', 'LARGE-FORK', 100, None) 
```
[^145]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.172)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.172, lines 12–19)*:
```
        super().__exit__(*args)
        self.session.close()  
    def commit(self):  
        self.session.commit()
    def rollback(self):  
        self.session.rollback()
The module defines a default session factory that will connect to
Postgres, but we allow that to be overridden in our integration tests
```
[^146]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Context Manager** *(p.170)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.170, lines 23–30)*:
```
    return batchref
Unit of Work and Its Context Manager
In our tests we’ve implicitly defined an interface for what a UoW
needs to do. Let’s make that explicit by using an abstract base class:
Abstract UoW context manager
(src/allocation/service_layer/unit_of_work.py)
class AbstractUnitOfWork(abc.ABC):
    batches: repository.AbstractRepository
```
[^147]
**Annotation:** This excerpt demonstrates 'context manager' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.187)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.187, lines 1–8)*:
```
TIP
The code for this chapter is in the appendix_csvs branch on GitHub:
git clone https://github.com/cosmicpython/code.git 
cd code 
git checkout appendix_csvs 
# or to code along, checkout the previous chapter: 
git checkout chapter_06_uow
Why Not Just Run Everything in a
```
[^148]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Datetime** *(p.160)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.160, lines 24–27)*:
```
    if eta is not None: 
        eta = datetime.fromisoformat(eta).date() 
    services.add_batch( 
        request.json['ref'], request.json['sku'], request.json['qty'], eta,
```
[^149]
**Annotation:** This excerpt demonstrates 'datetime' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 9: Going to Town on the Message Bus** *(pp.189–214)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^150]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: Commands and Command Handler** *(pp.215–234)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^151]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Event-Driven Architecture: Using Events to Integrate Microservices** *(pp.235–264)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^152]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 9: Going to Town on the Message Bus

*Source: Architecture Patterns with Python, pages 189–214*

### Chapter Summary
Expands on the message bus implementation with advanced event handling patterns. Covers event dispatching, handler registration, message routing, and building robust event processing pipelines. [^153]

### Concept-by-Concept Breakdown
#### **None** *(p.199)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.199, lines 6–13)*:
```
        product = uow.products.get(sku=sku) 
        if product is None: 
            product = model.Product(sku, batches=[]) 
            uow.products.add(product) 
        product.batches.append(model.Batch(ref, sku, qty, eta)) 
        uow.commit() 
 
 
```
[^154]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.196)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.196, lines 3–10)*:
```
class Product:
    def __init__(self, sku: str, batches: List[Batch]):
        self.sku = sku  
        self.batches = batches  
    def allocate(self, line: OrderLine) -> str:  
        try:
            batch = next(
                b for b in sorted(self.batches) if b.can_allocate(line)
```
[^155]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.191)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.191, lines 3–10)*:
```
object that contains other domain objects and lets us treat the whole
collection as a single unit.
The only way to modify the objects inside the aggregate is to load the
whole thing, and to call methods on the aggregate itself.
As a model gets more complex and grows more entity and value
objects, referencing each other in a tangled graph, it can be hard to
keep track of who can modify what. Especially when we have
collections in the model as we do (our batches are a collection), it’s a
```
[^156]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 15 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.208)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.208, lines 28–32)*:
```
    )
    assert version == 2  
    [exception] = exceptions
    assert 'could not serialize access due to concurrent update' in 
str(exception)
```
[^157]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.197)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.197, lines 5–12)*:
```
model. The word customer means different things to people in sales, customer service, logistics,
support, and so on. Attributes needed in one context are irrelevant in another; more perniciously,
concepts with the same name can have entirely different meanings in different contexts. Rather
than trying to build a single model (or class, or database) to capture all the use cases, it’s better
to have several models, draw boundaries around each context, and handle the translation
between different contexts explicitly.
This concept translates very well to the world of microservices, where each microservice is free
to have its own concept of “customer” and its own rules for translating that to and from other
```
[^158]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.189)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.189, lines 16–23)*:
```
update the state of the system, our code needs to ensure that we don’t
break the invariant, which is that the available quantity must be greater
than or equal to zero.
In a single-threaded, single-user application, it’s relatively easy for us
to maintain this invariant. We can just allocate stock one line at a time,
and raise an error if there’s no stock available.
This gets much harder when we introduce the idea of concurrency.
Suddenly we might be allocating stock for multiple order lines
```
[^159]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.196)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.196, lines 2–9)*:
```
Our chosen aggregate, Product (src/allocation/domain/model.py)
class Product:
    def __init__(self, sku: str, batches: List[Batch]):
        self.sku = sku  
        self.batches = batches  
    def allocate(self, line: OrderLine) -> str:  
        try:
            batch = next(
```
[^160]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.191)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.191, lines 9–16)*:
```
keep track of who can modify what. Especially when we have
collections in the model as we do (our batches are a collection), it’s a
good idea to nominate some entities to be the single entrypoint for
modifying their related objects. It makes the system conceptually
simpler and easy to reason about if you nominate some objects to be in
charge of consistency for the others.
For example, if we’re building a shopping site, the Cart might make a
good aggregate: it’s a collection of items that we can treat as a single
```
[^161]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Constructor** *(p.205)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.205, lines 23–30)*:
```
1. version_number lives in the domain; we add it to the
Product constructor, and Product.allocate() is
responsible for incrementing it.
2. The service layer could do it! The version number isn’t
strictly a domain concern, so instead our service layer could
assume that the current version number is attached to Product
by the repository, and the service layer will increment it
before it does the commit().
```
[^162]
**Annotation:** This excerpt demonstrates 'constructor' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.196)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.196, lines 3–10)*:
```
class Product:
    def __init__(self, sku: str, batches: List[Batch]):
        self.sku = sku  
        self.batches = batches  
    def allocate(self, line: OrderLine) -> str:  
        try:
            batch = next(
                b for b in sorted(self.batches) if b.can_allocate(line)
```
[^163]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.197)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.197, lines 20–27)*:
```
Once again, we find ourselves forced to say that we can’t give this issue the treatment it deserves
here, and we can only encourage you to read up on it elsewhere. The Fowler link at the start of
this sidebar is a good starting point, and either (or indeed, any) DDD book will have a chapter or
more on bounded contexts.
One Aggregate = One Repository
Once you define certain entities to be aggregates, we need to apply the
rule that they are the only entities that are publicly accessible to the
outside world. In other words, the only repositories we are allowed
```
[^164]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.208)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.208, lines 1–8)*:
```
uow.commit() 
    except Exception as e: 
        print(traceback.format_exc()) 
        exceptions.append(e)
Then we have our test invoke this slow allocation twice, concurrently,
using threads:
An integration test for concurrency behavior
(tests/integration/test_uow.py)
```
[^165]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 10 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.208)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.208, lines 1–8)*:
```
uow.commit() 
    except Exception as e: 
        print(traceback.format_exc()) 
        exceptions.append(e)
Then we have our test invoke this slow allocation twice, concurrently,
using threads:
An integration test for concurrency behavior
(tests/integration/test_uow.py)
```
[^166]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.196)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.196, lines 18–25)*:
```
for that SKU.
Finally, we can move the allocate() domain service to be a
method on the Product aggregate.
NOTE
This Product might not look like what you’d expect a Product model to look like.
No price, no description, no dimensions. Our allocation service doesn’t care about
any of those things. This is the power of bounded contexts; the concept of a
product in one app can be very different from another. See the following sidebar
```
[^167]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.191)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.191, lines 1–8)*:
```
The Aggregate pattern is a design pattern from the DDD community
that helps us to resolve this tension. An aggregate is just a domain
object that contains other domain objects and lets us treat the whole
collection as a single unit.
The only way to modify the objects inside the aggregate is to load the
whole thing, and to call methods on the aggregate itself.
As a model gets more complex and grows more entity and value
objects, referencing each other in a tangled graph, it can be hard to
```
[^168]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 10: Commands and Command Handler** *(pp.215–234)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^169]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Event-Driven Architecture: Using Events to Integrate Microservices** *(pp.235–264)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^170]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 12: Command-Query Responsibility Segregation (CQRS)** *(pp.265–288)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^171]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 10: Commands and Command Handler

*Source: Architecture Patterns with Python, pages 215–234*

### Chapter Summary
Introduces the Command pattern and command handlers as part of CQRS. Distinguishes commands (write operations) from queries, covers command validation, intent capture, and implementing a command bus for orchestrating business operations. [^172]

### Concept-by-Concept Breakdown
#### **None** *(p.232)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.232, lines 7–14)*:
```
    assert product.events[-1] == events.OutOfStock(sku="SMALL-FORK")  
    assert allocation is None
Our aggregate will expose a new attribute called .events that will
contain a list of facts about what has happened, in the form of
Event objects.
Here’s what the model looks like on the inside:
The model raises a domain event (src/allocation/domain/model.py)
class Product:
```
[^173]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.232)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.232, lines 14–21)*:
```
class Product:
    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):
        self.sku = sku
        self.batches = batches
        self.version_number = version_number
        self.events = []  # type: List[events.Event]  
    def allocate(self, line: OrderLine) -> str:
        try:
```
[^174]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.230)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.230, lines 10–17)*:
```
We want to apply the dependency inversion principle to notifications
so that our service layer depends on an abstraction, in the same way as
we avoid depending on the database by using a unit of work.
All Aboard the Message Bus!
The patterns we’re going to introduce here are Domain Events and the
Message Bus. We can implement them in a few ways, so we’ll show a
couple before settling on the one we like most.
The Model Records Events
```
[^175]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.234)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.234, lines 25–29)*:
```
not necessarily be Python services. Celery’s API for distributing tasks is essentially “function
name plus arguments,” which is more restrictive, and Python-only.
Option 1: The Service Layer Takes
Events from the Model and Puts Them on
the Message Bus
```
[^176]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.234)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.234, lines 5–12)*:
```
NOTE
Note that the message bus as implemented doesn’t give us concurrency because
only one handler will run at a time. Our objective isn’t to support parallel threads
but to separate tasks conceptually, and to keep each UoW as small as possible.
This helps us to understand the codebase because the “recipe” for how to run
each use case is written in a single place. See the following sidebar.
IS THIS LIKE CELERY?
Celery is a popular tool in the Python world for deferring self-contained chunks of work to an
```
[^177]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 14 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.232)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.232, lines 6–13)*:
```
    allocation = product.allocate(OrderLine('order2', 'SMALL-FORK', 1))
    assert product.events[-1] == events.OutOfStock(sku="SMALL-FORK")  
    assert allocation is None
Our aggregate will expose a new attribute called .events that will
contain a list of facts about what has happened, in the form of
Event objects.
Here’s what the model looks like on the inside:
The model raises a domain event (src/allocation/domain/model.py)
```
[^178]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.219)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.219, lines 20–21)*:
```
a system from many small components that interact through
asynchronous message passing.
```
[^179]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.232)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.232, lines 8–15)*:
```
    assert allocation is None
Our aggregate will expose a new attribute called .events that will
contain a list of facts about what has happened, in the form of
Event objects.
Here’s what the model looks like on the inside:
The model raises a domain event (src/allocation/domain/model.py)
class Product:
    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):
```
[^180]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.231)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.231, lines 8–15)*:
```
domain/events.py):
Event classes (src/allocation/domain/events.py)
from dataclasses import dataclass
class Event:  
    pass
@dataclass
class OutOfStock(Event):  
    sku: str
```
[^181]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.218)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.218, lines 14–21)*:
```
1  Perhaps we could get some ORM/SQLAlchemy magic to tell us when an object is dirty,
but how would that work in the generic case—for example, for a CsvRepository?
2  time.sleep() works well in our use case, but it’s not the most reliable or efficient way
to reproduce concurrency bugs. Consider using semaphores or similar synchronization
primitives shared between your threads to get better guarantees of behavior.
3  If you’re not using Postgres, you’ll need to read different documentation. Annoyingly,
different databases all have quite different definitions. Oracle’s SERIALIZABLE is
equivalent to Postgres’s REPEATABLE READ, for example.
```
[^182]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.232)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.232, lines 1–8)*:
```
Test our aggregate to raise events (tests/unit/test_product.py)
def test_records_out_of_stock_event_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    product = Product(sku="SMALL-FORK", batches=[batch])
    product.allocate(OrderLine('order1', 'SMALL-FORK', 10))
    allocation = product.allocate(OrderLine('order2', 'SMALL-FORK', 1))
    assert product.events[-1] == events.OutOfStock(sku="SMALL-FORK")  
    assert allocation is None
```
[^183]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.228)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.228, lines 9–16)*:
```
The domain model’s job is to know that we’re out of stock, but the
responsibility of sending an alert belongs elsewhere. We should be
able to turn this feature on or off, or to switch to SMS notifications
instead, without needing to change the rules of our domain model.
Or the Service Layer!
The requirement “Try to allocate some stock, and send an email if it
fails” is an example of workflow orchestration: it’s a set of steps that
the system has to follow to achieve a goal.
```
[^184]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.233)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.233, lines 1–8)*:
```
domain.
We’re also going to stop raising an exception for the out-of-stock
case. The event will do the job the exception was doing.
NOTE
We’re actually addressing a code smell we had until now, which is that we were
using exceptions for control flow. In general, if you’re implementing domain
events, don’t raise exceptions to describe the same domain concept. As you’ll see
later when we handle events in the Unit of Work pattern, it’s confusing to have to
```
[^185]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.233)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.233, lines 1–8)*:
```
domain.
We’re also going to stop raising an exception for the out-of-stock
case. The event will do the job the exception was doing.
NOTE
We’re actually addressing a code smell we had until now, which is that we were
using exceptions for control flow. In general, if you’re implementing domain
events, don’t raise exceptions to describe the same domain concept. As you’ll see
later when we handle events in the Unit of Work pattern, it’s confusing to have to
```
[^186]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.231)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.231, lines 5–12)*:
```
We could store them in model.py, but we may as well keep them in
their own file (this might be a good time to consider refactoring out a
directory called domain so that we have domain/model.py and
domain/events.py):
Event classes (src/allocation/domain/events.py)
from dataclasses import dataclass
class Event:  
    pass
```
[^187]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 11: Event-Driven Architecture: Using Events to Integrate Microservices** *(pp.235–264)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^188]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 12: Command-Query Responsibility Segregation (CQRS)** *(pp.265–288)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^189]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 13: Dependency Injection (and Bootstrapping)** *(pp.289–497)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^190]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 11: Event-Driven Architecture: Using Events to Integrate Microservices

*Source: Architecture Patterns with Python, pages 235–264*

### Chapter Summary
Explores event-driven architecture for integrating microservices. Covers distributed system patterns, async communication between services, eventual consistency, service choreography vs orchestration, and bounded contexts with anti-corruption layers. [^191]

### Concept-by-Concept Breakdown
#### **None** *(p.259)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.259, lines 26–31)*:
```
         uow = FakeUnitOfWork() 
-        services.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)
+        messagebus.handle(
+            events.BatchCreated("b1", "CRUNCHY-ARMCHAIR", 100, None), uow
+        ) 
         assert uow.products.get("CRUNCHY-ARMCHAIR") is not None
```
[^192]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.239)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.239, lines 13–20)*:
```
class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session
    def _add(self, product):  
        self.session.add(product)
    def _get(self, sku):  
        return self.session.query(model.Product).filter_by(sku=sku).first()
```
[^193]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.242)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.242, lines 29–32)*:
```
experience it’s not a lot of work. Once your project is up and running,
the interface for your repository and UoW abstractions really don’t
change much. And if you’re using ABCs, they’ll help remind you when
things get out of sync.
```
[^194]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.257)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.257, lines 6–13)*:
```
Along the way, we’ve made our service-layer’s API more structured
and more consistent. It was a scattering of primitives, and now it uses
well-defined objects (see the following sidebar).
FROM DOMAIN OBJECTS, VIA PRIMITIVE OBSESSION, TO
EVENTS AS AN INTERFACE
Some of you may remember “Fully Decoupling the Service-Layer Tests from the Domain”, in
which we changed our service-layer API from being in terms of domain objects to primitives. And
now we’re moving back, but to different objects? What gives?
```
[^195]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 12 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.260)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.260, lines 1–8)*:
```
assert uow.committed 
 
... 
 
 class TestAllocate: 
 
     def test_returns_allocation(self): 
         uow = FakeUnitOfWork() 
```
[^196]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.244)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.244, lines 39–46)*:
```
web endpoints 
(adding asynchronous processing 
is possible but makes things even 
more confusing).
More generally, event-driven 
workflows can be confusing 
because after things 
are split across a chain of multiple 
```
[^197]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.238)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.238, lines 12–19)*:
```
That relies on the repository keeping track of aggregates that have
been loaded using a new attribute, .seen, as you’ll see in the next
listing.
NOTE
Are you wondering what happens if one of the handlers fails? We’ll discuss error
handling in detail in Chapter 10.
Repository tracks aggregates that pass through it
(src/allocation/adapters/repository.py)
```
[^198]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.255)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.255, lines 4–11)*:
```
(src/allocation/domain/events.py)
@dataclass
class BatchCreated(Event): 
    ref: str 
    sku: str 
    qty: int 
    eta: Optional[date] = None 
 
```
[^199]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.239)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.239, lines 1–8)*:
```
self.seen.add(product)
    def get(self, sku) -> model.Product:  
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product
    @abc.abstractmethod
    def _add(self, product: model.Product):  
```
[^200]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.235)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.235, lines 26–30)*:
```
We keep the try/finally from our ugly earlier implementation
(we haven’t gotten rid of all exceptions yet, just OutOfStock).
But now, instead of depending directly on an email infrastructure,
the service layer is just in charge of passing events from the model
up to the message bus.
```
[^201]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.235)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.235, lines 26–30)*:
```
We keep the try/finally from our ugly earlier implementation
(we haven’t gotten rid of all exceptions yet, just OutOfStock).
But now, instead of depending directly on an email infrastructure,
the service layer is just in charge of passing events from the model
up to the message bus.
```
[^202]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.235)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.235, lines 23–30)*:
```
            return batchref
        finally:  
            messagebus.handle(product.events)  
We keep the try/finally from our ugly earlier implementation
(we haven’t gotten rid of all exceptions yet, just OutOfStock).
But now, instead of depending directly on an email infrastructure,
the service layer is just in charge of passing events from the model
up to the message bus.
```
[^203]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.246)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.246, lines 3–10)*:
```
Code gets tangled up when we mix multiple concerns in one place. Events can help us to
keep things tidy by separating primary use cases from secondary ones. We also use events
for communicating between aggregates so that we don’t need to run long-running
transactions that lock against multiple tables.
A message bus routes messages to handlers
You can think of a message bus as a dict that maps from events to their consumers. It
doesn’t “know” anything about the meaning of events; it’s just a piece of dumb infrastructure
for getting messages around the system.
```
[^204]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.253)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.253, lines 7–14)*:
```
kinds of flows through our system:
API calls that are handled by a service-layer function
Internal events (which might be raised as a side effect of a
service-layer function) and their handlers (which in turn call
service-layer functions)
Wouldn’t it be easier if everything was an event handler? If we rethink
our API calls as capturing events, the service-layer functions can be
event handlers too, and we no longer need to make a distinction
```
[^205]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Global** *(p.252)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.252, lines 1–8)*:
```
A global shortage of sequins means we’re unable to
manufacture our next batch of SPARKLY-BOOKCASE.
In these types of situations, we learn about the need to change batch
quantities when they’re already in the system. Perhaps someone made
a mistake on the number in the manifest, or perhaps some sofas fell off
a truck. Following a conversation with the business,  we model the
situation as in Figure 9-3.
Figure 9-3. Batch quantity changed means deallocate and reallocate
```
[^206]
**Annotation:** This excerpt demonstrates 'global' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 12: Command-Query Responsibility Segregation (CQRS)** *(pp.265–288)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^207]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 13: Dependency Injection (and Bootstrapping)** *(pp.289–497)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^208]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 12: Command-Query Responsibility Segregation (CQRS)

*Source: Architecture Patterns with Python, pages 265–288*

### Chapter Summary
Details Command-Query Responsibility Segregation (CQRS) pattern. Covers separating read and write models, building projections and materialized views, denormalization strategies, and optimizing for scalability with separate query and command sides. [^209]

### Concept-by-Concept Breakdown
#### **None** *(p.265)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.265, lines 4–11)*:
```
        messagebus.handle(
            events.BatchCreated("batch1", "ADORABLE-SETTEE", 100, None), uow
        )
        [batch] = uow.products.get(sku="ADORABLE-SETTEE").batches
        assert batch.available_quantity == 100  
        messagebus.handle(events.BatchQuantityChanged("batch1", 50), uow)
        assert batch.available_quantity == 50  
    def test_reallocates_if_necessary(self):
```
[^210]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.270)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.270, lines 7–14)*:
```
 
    def __init__(self): 
        super().__init__() 
        self.events_published = []  # type: List[events.Event] 
 
    def publish_events(self): 
        for product in self.products.seen: 
            while product.events: 
```
[^211]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.265)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.265, lines 1–8)*:
```
class TestChangeBatchQuantity:
    def test_changes_available_quantity(self):
        uow = FakeUnitOfWork()
        messagebus.handle(
            events.BatchCreated("batch1", "ADORABLE-SETTEE", 100, None), uow
        )
        [batch] = uow.products.get(sku="ADORABLE-SETTEE").batches
        assert batch.available_quantity == 100  
```
[^212]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.265)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.265, lines 7–14)*:
```
        [batch] = uow.products.get(sku="ADORABLE-SETTEE").batches
        assert batch.available_quantity == 100  
        messagebus.handle(events.BatchQuantityChanged("batch1", 50), uow)
        assert batch.available_quantity == 50  
    def test_reallocates_if_necessary(self):
        uow = FakeUnitOfWork()
        event_history = [
            events.BatchCreated("batch1", "INDIFFERENT-TABLE", 50, None),
```
[^213]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.278)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.278, lines 14–21)*:
```
Pulling out some commands (src/allocation/domain/commands.py)
class Command:
    pass
@dataclass
class Allocate(Command):  
    orderid: str
    sku: str
    qty: int
```
[^214]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.280)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.280, lines 17–24)*:
```
            logger.exception('Exception handling event %s', event)
            continue  
Events go to a dispatcher that can delegate to multiple handlers per
event.
It catches and logs errors but doesn’t let them interrupt message
processing.
And here’s how we do commands:
Commands reraise exceptions
```
[^215]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.267)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.267, lines 1–8)*:
```
def _add(self, product: model.Product): 
        raise NotImplementedError 
 
    @abc.abstractmethod 
    def _get(self, sku) -> model.Product: 
        raise NotImplementedError 
 
    @abc.abstractmethod 
```
[^216]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Elif** *(p.279)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.279, lines 18–25)*:
```
            handle_event(message, queue, uow)  
        elif isinstance(message, commands.Command):
            cmd_result = handle_command(message, queue, uow)  
            results.append(cmd_result)
        else:
            raise Exception(f'{message} was not an Event or Command')
    return results
It still has a main handle() entrypoint that takes a message, which
```
[^217]
**Annotation:** This excerpt demonstrates 'elif' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.279)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.279, lines 21–26)*:
```
            results.append(cmd_result)
        else:
            raise Exception(f'{message} was not an Event or Command')
    return results
It still has a main handle() entrypoint that takes a message, which
may be a command or an event.
```
[^218]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Error Handling** *(p.278)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.278, lines 6–13)*:
```
Imperative mood
Error handling
Fail independently
Fail noisily
Sent to
All listeners
One recipient
What kinds of commands do we have in our system right now?
```
[^219]
**Annotation:** This excerpt demonstrates 'error handling' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.280)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.280, lines 15–22)*:
```
            queue.extend(uow.collect_new_events())
        except Exception:
            logger.exception('Exception handling event %s', event)
            continue  
Events go to a dispatcher that can delegate to multiple handlers per
event.
It catches and logs errors but doesn’t let them interrupt message
processing.
```
[^220]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.280)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.280, lines 15–22)*:
```
            queue.extend(uow.collect_new_events())
        except Exception:
            logger.exception('Exception handling event %s', event)
            continue  
Events go to a dispatcher that can delegate to multiple handlers per
event.
It catches and logs errors but doesn’t let them interrupt message
processing.
```
[^221]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.285)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.285, lines 14–21)*:
```
order was created.
Finally, we send an email to the customer when they become a VIP.
Using this code, we can gain some intuition about error handling in an
event-driven system.
In our current implementation, we raise events about an aggregate after
we persist our state to the database. What if we raised those events
before we persisted, and committed all our changes at the same time?
That way, we could be sure that all the work was complete. Wouldn’t
```
[^222]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.286)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.286, lines 14–21)*:
```
to reason about our systems as they grow larger and more complex.
Recovering from Errors Synchronously
Hopefully we’ve convinced you that it’s OK for events to fail
independently from the commands that raised them. What should we
do, then, to make sure we can recover from errors when they
inevitably occur?
The first thing we need is to know when an error has occurred, and for
that we usually rely on logs.
```
[^223]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.287)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.287, lines 1–8)*:
```
Current handle function
(src/allocation/service_layer/messagebus.py)
def handle_event( 
    event: events.Event, 
    queue: List[Message], 
    uow: unit_of_work.AbstractUnitOfWork
): 
    for handler in EVENT_HANDLERS[type(event)]: 
```
[^224]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 13: Dependency Injection (and Bootstrapping)** *(pp.289–497)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^225]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 13: Dependency Injection (and Bootstrapping)

*Source: Architecture Patterns with Python, pages 289–497*

### Chapter Summary
Covers dependency injection and application bootstrapping. Discusses composition root pattern, IoC containers, factory patterns, managing dependencies for testability, and properly wiring up application components during initialization. [^226]

### Concept-by-Concept Breakdown
#### **None** *(p.355)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.355, lines 12–19)*:
```
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),  
        send_mail=lambda *args: None,  
        publish=lambda *args: None,  
    )
    yield bus
    clear_mappers()
def test_allocations_view(sqlite_bus):
    sqlite_bus.handle(commands.CreateBatch('sku1batch', 'sku1', 50, None))
```
[^227]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.421)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.421, lines 15–22)*:
```
class DjangoUnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        self.batches = repository.DjangoRepository()
        transaction.set_autocommit(False)  
        return super().__enter__()
    def __exit__(self, *args):
        super().__exit__(*args)
        transaction.set_autocommit(True)
```
[^228]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Eq__** *(p.417)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.417, lines 23–30)*:
```
    expected = model.Batch("batch1", sku, 100, eta=None) 
    assert retrieved == expected  # Batch.__eq__ only compares reference 
    assert retrieved.sku == expected.sku 
    assert retrieved._purchased_quantity == expected._purchased_quantity 
    assert retrieved._allocations == { 
        model.OrderLine("order1", sku, 12), 
    }
Here’s how the actual repository ends up looking:
```
[^229]
**Annotation:** This excerpt demonstrates '__eq__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.421)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.421, lines 19–26)*:
```
        return super().__enter__()
    def __exit__(self, *args):
        super().__exit__(*args)
        transaction.set_autocommit(True)
    def commit(self):
        for batch in self.batches.seen:  
            self.batches.update(batch)  
        transaction.commit()  
```
[^230]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.415)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.415, lines 8–15)*:
```
│   ├── allocation
│   │   ├── __init__.py
│   │   ├── adapters
│   │   │   ├── __init__.py
...
│   ├── djangoproject
│   │   ├── alloc
│   │   │   ├── __init__.py
```
[^231]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.410)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.410, lines 1–8)*:
```
if __name__ == '__main__': 
    main(sys.argv[1])
It’s not looking too bad! And we’re reusing our domain model objects
and our domain service.
But it’s not going to work. Existing allocations need to also be part of
our permanent CSV storage. We can write a second test to force us to
improve things:
And another one, with existing allocations (tests/e2e/test_csv.py)
```
[^232]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.354)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.354, lines 11–18)*:
```
+from allocation import bootstrap, views 
 app = Flask(__name__) 
-orm.start_mappers()  
+bus = bootstrap.bootstrap() 
 @app.route("/add_batch", methods=['POST']) 
@@ -19,8 +16,7 @@ def add_batch(): 
     cmd = commands.CreateBatch( 
         request.json['ref'], request.json['sku'], request.json['qty'], eta, 
```
[^233]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.442)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.442, lines 1–8)*:
```
choosing right abstraction, Choosing the Right Abstraction(s)-
Implementing Our Chosen Abstractions
explicit dependencies are more abstract, Aren’t Explicit
Dependencies Totally Weird and Java-y?
implementing chosen abstraction, Implementing Our Chosen
Abstractions-Wrap-Up
edge-to-edge testing with fakes and dependency injection,
Testing Edge to Edge with Fakes and Dependency Injection-
```
[^234]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.355)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.355, lines 12–19)*:
```
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),  
        send_mail=lambda *args: None,  
        publish=lambda *args: None,  
    )
    yield bus
    clear_mappers()
def test_allocations_view(sqlite_bus):
    sqlite_bus.handle(commands.CreateBatch('sku1batch', 'sku1', 50, None))
```
[^235]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.349)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.349, lines 5–12)*:
```
things like setting up the logging module.
We can use the argument defaults to define what the
normal/production defaults are. It’s nice to have them in a single
place, but sometimes dependencies have some side effects at
construction time, in which case you might prefer to default them to
None instead.
We build up our injected versions of the handler mappings by using
a function called inject_dependencies(), which we’ll show
```
[^236]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.383)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.383, lines 1–8)*:
```
CASE STUDY: DAVID SEDDON ON TAKING SMALL STEPS
Hi, I’m David, one of the tech reviewers on this book. I’ve worked on several complex Django
monoliths, and so I’ve known the pain that Bob and Harry have made all sorts of grand promises
about soothing.
When I was first exposed to the patterns described here, I was rather excited. I had successfully
used some of the techniques already on smaller projects, but here was a blueprint for much
larger, database-backed systems like the one I work on in my day job. So I started trying to figure
out how I could implement that blueprint at my current organization.
```
[^237]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 26 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.317)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.317, lines 11–18)*:
```
    r = api_client.post_to_allocate(orderid, sku, qty=3) 
    assert r.status_code == 202 
 
    r = api_client.get_allocation(orderid) 
    assert r.ok 
    assert r.json() == [ 
        {'sku': sku, 'batchref': earlybatch}, 
    ] 
```
[^238]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.332)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.332, lines 1–8)*:
```
the implementation: setup puts messages on the message bus, and the
assertions are against our view.
TIP
Event handlers are a great way to manage updates to a read model, if you decide
you need one. They also make it easy to change the implementation of that read
model at a later date.
EXERCISE FOR THE READER
Implement another view, this time to show the allocation for a single order line.
```
[^239]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.452)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.452, lines 1–8)*:
```
microservices as, The Alternative: Temporal Decoupling Using
Asynchronous Messaging
recap, Wrap-Up
constraints, Invariants, Constraints, and Consistency
context manager, Unit of Work Pattern
starting Unit of Work as, The Unit of Work Collaborates with the
Repository
Unit of Work and, Unit of Work and Its Context Manager-Fake
```
[^240]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.394)*

**Verbatim Educational Excerpt** *(Architecture Patterns, p.394, lines 10–17)*:
```
Entity
A domain object whose attributes may 
change but that has a recognizable identity 
over time.
Value 
object
An immutable domain object whose attributes 
entirely define it. It is fungible with other 
```
[^241]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---


---

### **Footnotes**

[^1]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 1, lines 1–25).
[^2]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 20, lines 11–18).
[^3]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 24, lines 18–25).
[^4]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 21, lines 5–12).
[^5]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 9, lines 21–24).
[^6]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 20, lines 13–20).
[^7]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 22, lines 4–11).
[^8]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 11, lines 7–14).
[^9]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 6, lines 1–8).
[^10]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 12, lines 23–24).
[^11]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 11, lines 16–23).
[^12]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 18, lines 14–20).
[^13]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 2, lines 19–22).
[^14]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 9, lines 19–24).
[^15]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 3, lines 15–22).
[^16]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 3, lines 15–22).
[^17]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 25, lines 1–1).
[^18]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 47, lines 1–1).
[^19]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 59, lines 1–1).
[^20]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 25, lines 1–25).
[^21]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 31, lines 1–8).
[^22]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 43, lines 11–13).
[^23]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 36, lines 1–8).
[^24]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 36, lines 12–19).
[^25]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 26, lines 3–10).
[^26]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 32, lines 18–23).
[^27]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 34, lines 11–18).
[^28]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 45, lines 5–9).
[^29]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 32, lines 9–16).
[^30]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 36, lines 10–17).
[^31]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 33, lines 1–6).
[^32]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 34, lines 6–13).
[^33]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 28, lines 2–9).
[^34]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 25, lines 8–15).
[^35]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 25, lines 18–25).
[^36]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 47, lines 1–1).
[^37]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 59, lines 1–1).
[^38]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 87, lines 1–1).
[^39]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 47, lines 1–25).
[^40]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 57, lines 24–31).
[^41]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 56, lines 7–14).
[^42]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 56, lines 25–31).
[^43]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 54, lines 2–9).
[^44]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 57, lines 13–20).
[^45]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 56, lines 1–8).
[^46]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 56, lines 20–27).
[^47]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 57, lines 4–11).
[^48]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 48, lines 15–22).
[^49]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 48, lines 15–22).
[^50]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 55, lines 2–9).
[^51]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 49, lines 15–20).
[^52]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 56, lines 16–23).
[^53]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 56, lines 17–24).
[^54]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 56, lines 28–31).
[^55]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 59, lines 1–1).
[^56]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 87, lines 1–1).
[^57]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 105, lines 1–1).
[^58]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 59, lines 1–25).
[^59]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 76, lines 18–23).
[^60]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 69, lines 5–12).
[^61]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 66, lines 2–9).
[^62]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 61, lines 18–25).
[^63]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 74, lines 4–11).
[^64]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 85, lines 20–27).
[^65]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 66, lines 1–8).
[^66]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 63, lines 12–19).
[^67]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 66, lines 8–15).
[^68]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 83, lines 5–12).
[^69]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 70, lines 2–9).
[^70]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 62, lines 27–28).
[^71]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 64, lines 25–26).
[^72]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 59, lines 5–12).
[^73]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 61, lines 4–11).
[^74]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 87, lines 1–1).
[^75]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 105, lines 1–1).
[^76]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 133, lines 1–1).
[^77]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 87, lines 1–25).
[^78]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 91, lines 2–9).
[^79]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 92, lines 10–17).
[^80]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 93, lines 8–15).
[^81]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 103, lines 2–9).
[^82]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 96, lines 2–9).
[^83]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 89, lines 1–8).
[^84]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 92, lines 10–17).
[^85]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 90, lines 14–19).
[^86]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 92, lines 25–30).
[^87]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 104, lines 1–8).
[^88]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 88, lines 8–15).
[^89]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 93, lines 8–15).
[^90]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 89, lines 1–8).
[^91]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 103, lines 16–19).
[^92]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 101, lines 25–27).
[^93]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 105, lines 1–1).
[^94]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 133, lines 1–1).
[^95]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 155, lines 1–1).
[^96]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 105, lines 1–25).
[^97]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 126, lines 13–20).
[^98]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 128, lines 3–10).
[^99]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 129, lines 12–19).
[^100]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 105, lines 4–11).
[^101]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 118, lines 19–24).
[^102]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 107, lines 2–9).
[^103]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 108, lines 1–8).
[^104]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 119, lines 10–17).
[^105]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 119, lines 3–10).
[^106]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 118, lines 10–17).
[^107]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 116, lines 5–12).
[^108]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 110, lines 13–20).
[^109]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 116, lines 8–15).
[^110]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 107, lines 15–22).
[^111]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 130, lines 27–31).
[^112]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 133, lines 1–1).
[^113]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 155, lines 1–1).
[^114]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 189, lines 1–1).
[^115]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 133, lines 1–25).
[^116]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 134, lines 2–9).
[^117]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 141, lines 1–8).
[^118]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 136, lines 7–14).
[^119]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 142, lines 2–9).
[^120]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 138, lines 8–15).
[^121]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 136, lines 1–8).
[^122]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 153, lines 6–13).
[^123]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 152, lines 31–33).
[^124]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 141, lines 24–31).
[^125]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 149, lines 7–12).
[^126]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 152, lines 29–33).
[^127]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 133, lines 13–20).
[^128]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 141, lines 26–33).
[^129]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 141, lines 26–33).
[^130]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 141, lines 23–30).
[^131]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 155, lines 1–1).
[^132]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 189, lines 1–1).
[^133]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 215, lines 1–1).
[^134]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 155, lines 1–25).
[^135]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 160, lines 1–8).
[^136]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 172, lines 6–13).
[^137]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 171, lines 1–8).
[^138]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 172, lines 4–11).
[^139]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 183, lines 8–15).
[^140]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 172, lines 10–17).
[^141]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 180, lines 5–12).
[^142]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 174, lines 1–8).
[^143]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 158, lines 7–14).
[^144]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 171, lines 8–15).
[^145]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 176, lines 1–8).
[^146]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 172, lines 12–19).
[^147]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 170, lines 23–30).
[^148]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 187, lines 1–8).
[^149]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 160, lines 24–27).
[^150]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 189, lines 1–1).
[^151]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 215, lines 1–1).
[^152]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 235, lines 1–1).
[^153]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 189, lines 1–25).
[^154]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 199, lines 6–13).
[^155]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 196, lines 3–10).
[^156]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 191, lines 3–10).
[^157]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 208, lines 28–32).
[^158]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 197, lines 5–12).
[^159]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 189, lines 16–23).
[^160]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 196, lines 2–9).
[^161]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 191, lines 9–16).
[^162]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 205, lines 23–30).
[^163]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 196, lines 3–10).
[^164]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 197, lines 20–27).
[^165]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 208, lines 1–8).
[^166]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 208, lines 1–8).
[^167]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 196, lines 18–25).
[^168]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 191, lines 1–8).
[^169]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 215, lines 1–1).
[^170]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 235, lines 1–1).
[^171]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 265, lines 1–1).
[^172]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 215, lines 1–25).
[^173]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 232, lines 7–14).
[^174]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 232, lines 14–21).
[^175]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 230, lines 10–17).
[^176]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 234, lines 25–29).
[^177]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 234, lines 5–12).
[^178]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 232, lines 6–13).
[^179]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 219, lines 20–21).
[^180]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 232, lines 8–15).
[^181]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 231, lines 8–15).
[^182]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 218, lines 14–21).
[^183]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 232, lines 1–8).
[^184]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 228, lines 9–16).
[^185]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 233, lines 1–8).
[^186]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 233, lines 1–8).
[^187]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 231, lines 5–12).
[^188]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 235, lines 1–1).
[^189]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 265, lines 1–1).
[^190]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 289, lines 1–1).
[^191]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 235, lines 1–25).
[^192]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 259, lines 26–31).
[^193]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 239, lines 13–20).
[^194]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 242, lines 29–32).
[^195]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 257, lines 6–13).
[^196]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 260, lines 1–8).
[^197]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 244, lines 39–46).
[^198]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 238, lines 12–19).
[^199]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 255, lines 4–11).
[^200]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 239, lines 1–8).
[^201]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 235, lines 26–30).
[^202]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 235, lines 26–30).
[^203]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 235, lines 23–30).
[^204]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 246, lines 3–10).
[^205]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 253, lines 7–14).
[^206]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 252, lines 1–8).
[^207]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 265, lines 1–1).
[^208]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 289, lines 1–1).
[^209]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 265, lines 1–25).
[^210]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 265, lines 4–11).
[^211]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 270, lines 7–14).
[^212]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 265, lines 1–8).
[^213]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 265, lines 7–14).
[^214]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 278, lines 14–21).
[^215]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 280, lines 17–24).
[^216]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 267, lines 1–8).
[^217]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 279, lines 18–25).
[^218]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 279, lines 21–26).
[^219]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 278, lines 6–13).
[^220]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 280, lines 15–22).
[^221]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 280, lines 15–22).
[^222]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 285, lines 14–21).
[^223]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 286, lines 14–21).
[^224]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 287, lines 1–8).
[^225]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 289, lines 1–1).
[^226]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 289, lines 1–25).
[^227]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 355, lines 12–19).
[^228]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 421, lines 15–22).
[^229]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 417, lines 23–30).
[^230]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 421, lines 19–26).
[^231]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 415, lines 8–15).
[^232]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 410, lines 1–8).
[^233]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 354, lines 11–18).
[^234]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 442, lines 1–8).
[^235]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 355, lines 12–19).
[^236]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 349, lines 5–12).
[^237]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 383, lines 1–8).
[^238]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 317, lines 11–18).
[^239]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 332, lines 1–8).
[^240]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 452, lines 1–8).
[^241]: Percival, Harry and Gregory, Bob. *Architecture Patterns with Python*. (JSON `Architecture Patterns with Python.json`, p. 394, lines 10–17).
