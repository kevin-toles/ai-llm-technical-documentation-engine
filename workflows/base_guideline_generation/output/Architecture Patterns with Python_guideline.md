# Comprehensive Python Guidelines — None (Chapters 1-41)

*Source: None, Chapters 1-41*

---

## Chapter 1: A Python Q&A Session

*Source: None, pages 16–44*

### Chapter Summary
Chapter 1 content. [^1]

### Concept-by-Concept Breakdown
#### **Gil** *(p.31)*

**Verbatim Educational Excerpt** *(None, p.31, lines 1–8)*:
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
[^2]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.20)*

**Verbatim Educational Excerpt** *(None, p.20, lines 11–18)*:
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
[^3]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.36)*

**Verbatim Educational Excerpt** *(None, p.36, lines 1–8)*:
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
[^4]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.36)*

**Verbatim Educational Excerpt** *(None, p.36, lines 12–19)*:
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
[^5]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.21)*

**Verbatim Educational Excerpt** *(None, p.21, lines 5–12)*:
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
[^6]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 11 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.20)*

**Verbatim Educational Excerpt** *(None, p.20, lines 13–20)*:
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
[^7]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.22)*

**Verbatim Educational Excerpt** *(None, p.22, lines 4–11)*:
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
[^8]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.24)*

**Verbatim Educational Excerpt** *(None, p.24, lines 19–26)*:
```
abstraction around persistent storage, and we build a service layer
to define the entrypoints to our system and capture the primary use
cases. We show how this layer makes it easy to build thin
entrypoints to our system, whether it’s a Flask API or a CLI.
Some thoughts on testing and abstractions (Chapters 3 and 6)
After presenting the first abstraction (the Repository pattern), we
take the opportunity for a general discussion of how to choose
abstractions, and what their role is in choosing how our software
```
[^9]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Duck Typing** *(p.36)*

**Verbatim Educational Excerpt** *(None, p.36, lines 10–17)*:
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
[^10]
**Annotation:** This excerpt demonstrates 'duck typing' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.18)*

**Verbatim Educational Excerpt** *(None, p.18, lines 14–20)*:
```
all these questions.
Bob ended up a software architect because nobody else on his team
was doing it. He turned out to be pretty bad at it, but he was lucky
enough to run into Ian Cooper, who taught him new ways of writing
and thinking about code.
Managing Complexity, Solving Business
Problems
```
[^11]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Encapsulation** *(p.34)*

**Verbatim Educational Excerpt** *(None, p.34, lines 6–13)*:
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
[^12]
**Annotation:** This excerpt demonstrates 'encapsulation' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.28)*

**Verbatim Educational Excerpt** *(None, p.28, lines 2–9)*:
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
[^13]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.25)*

**Verbatim Educational Excerpt** *(None, p.25, lines 8–15)*:
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
[^14]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.25)*

**Verbatim Educational Excerpt** *(None, p.25, lines 18–25)*:
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
[^15]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.36)*

**Verbatim Educational Excerpt** *(None, p.36, lines 11–18)*:
```
can also happily rely on duck typing.
The abstraction can just mean “the public API of the thing you’re using”—a function name plus
some arguments, for example.
Most of the patterns in this book involve choosing an abstraction, so
you’ll see plenty of examples in each chapter. In addition, Chapter 3
specifically discusses some general heuristics for choosing
abstractions.
Layering
```
[^16]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 2: How Python Runs Programs** *(pp.45–76)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^17]

**Annotation:** Forward reference: Chapter 2 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 3: How You Run Programs** *(pp.77–108)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^18]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Introducing Python Object Types** *(pp.109–140)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^19]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 2: How Python Runs Programs

*Source: None, pages 45–76*

### Chapter Summary
Chapter 2 content. [^20]

### Concept-by-Concept Breakdown
#### **Gil** *(p.76)*

**Verbatim Educational Excerpt** *(None, p.76, lines 18–23)*:
```
external state.
We expect to be working in an agile manner, so our priority is to get to
a minimum viable product as quickly as possible. In our case, that’s
going to be a web API. In a real project, you might dive straight in
with some end-to-end tests and start plugging in a web framework,
test-driving things outside-in.
```
[^21]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.69)*

**Verbatim Educational Excerpt** *(None, p.69, lines 5–12)*:
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
[^22]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Eq__** *(p.66)*

**Verbatim Educational Excerpt** *(None, p.66, lines 2–9)*:
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
[^23]
**Annotation:** This excerpt demonstrates '__eq__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.56)*

**Verbatim Educational Excerpt** *(None, p.56, lines 7–14)*:
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
[^24]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.74)*

**Verbatim Educational Excerpt** *(None, p.74, lines 4–11)*:
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
[^25]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.56)*

**Verbatim Educational Excerpt** *(None, p.56, lines 25–31)*:
```
For domain models, they can sometimes help to clarify or
document what the expected arguments are, and people with IDEs
are often grateful for them. You may decide the price paid in terms
of readability is too high.
Our implementation here is trivial: a Batch just wraps an integer
available_quantity, and we decrement that value on allocation.
2
```
[^26]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.66)*

**Verbatim Educational Excerpt** *(None, p.66, lines 1–8)*:
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
[^27]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 16 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.63)*

**Verbatim Educational Excerpt** *(None, p.63, lines 12–19)*:
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
[^28]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.66)*

**Verbatim Educational Excerpt** *(None, p.66, lines 8–15)*:
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
[^29]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.56)*

**Verbatim Educational Excerpt** *(None, p.56, lines 1–8)*:
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
[^30]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.70)*

**Verbatim Educational Excerpt** *(None, p.70, lines 2–9)*:
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
[^31]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.62)*

**Verbatim Educational Excerpt** *(None, p.62, lines 27–28)*:
```
from typing import NamedTuple
from collections import namedtuple
```
[^32]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.64)*

**Verbatim Educational Excerpt** *(None, p.64, lines 25–26)*:
```
But what about Harry as a person? People do change their names, and
their marital status, and even their gender, but we continue to recognize
```
[^33]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.45)*

**Verbatim Educational Excerpt** *(None, p.45, lines 5–9)*:
```
the Flask API, the ORM, and Postgres—for a totally different
I/O model involving a CLI and CSVs.
Finally, Appendix D may be of interest if you’re wondering
how these patterns might look if using Django instead of Flask
and SQLAlchemy.
```
[^34]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Datetime** *(p.56)*

**Verbatim Educational Excerpt** *(None, p.56, lines 20–27)*:
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
[^35]
**Annotation:** This excerpt demonstrates 'datetime' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 3: How You Run Programs** *(pp.77–108)*

This later chapter builds upon the concepts introduced here, particularly: None, __eq__, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^36]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __eq__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Introducing Python Object Types** *(pp.109–140)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^37]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Numeric Types** *(pp.141–175)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^38]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 3: How You Run Programs

*Source: None, pages 77–108*

### Chapter Summary
Chapter 3 content. [^39]

### Concept-by-Concept Breakdown
#### **None** *(p.91)*

**Verbatim Educational Excerpt** *(None, p.91, lines 2–9)*:
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
[^40]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Eq__** *(p.92)*

**Verbatim Educational Excerpt** *(None, p.92, lines 10–17)*:
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
[^41]
**Annotation:** This excerpt demonstrates '__eq__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.93)*

**Verbatim Educational Excerpt** *(None, p.93, lines 8–15)*:
```
 
    def __init__(self, session): 
        self.session = session 
 
    def add(self, batch): 
        self.session.add(batch) 
 
    def get(self, reference): 
```
[^42]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.103)*

**Verbatim Educational Excerpt** *(None, p.103, lines 2–9)*:
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
[^43]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.85)*

**Verbatim Educational Excerpt** *(None, p.85, lines 20–27)*:
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
[^44]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.107)*

**Verbatim Educational Excerpt** *(None, p.107, lines 2–9)*:
```
 
    # Walk the target folder and get the filenames and hashes 
    for folder, _, files in os.walk(dest): 
        for fn in files: 
            dest_path = Path(folder) / fn 
            dest_hash = hash_file(dest_path) 
            seen.add(dest_hash) 
 
```
[^45]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 17 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.92)*

**Verbatim Educational Excerpt** *(None, p.92, lines 10–17)*:
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
[^46]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.90)*

**Verbatim Educational Excerpt** *(None, p.90, lines 14–19)*:
```
is correctly integrated with the database; hence, the tests tend to mix
raw SQL with calls and assertions on our own code.
TIP
Unlike the ORM tests from earlier, these tests are good candidates for staying
part of your codebase longer term, particularly if any parts of your domain model
mean the object-relational map is nontrivial.
```
[^47]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.92)*

**Verbatim Educational Excerpt** *(None, p.92, lines 25–30)*:
```
remember, Batch is an entity, and we have a custom eq for it).
So we also explicitly check on its major attributes, including
._allocations, which is a Python set of OrderLine value
objects.
Whether or not you painstakingly write tests for every model is a
judgment call. Once you have one class tested for create/modify/save,
```
[^48]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.104)*

**Verbatim Educational Excerpt** *(None, p.104, lines 1–8)*:
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
[^49]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.83)*

**Verbatim Educational Excerpt** *(None, p.83, lines 5–12)*:
```
Django ORM example
class Order(models.Model): 
    pass 
 
class OrderLine(models.Model): 
    sku = models.CharField(max_length=255) 
    qty = models.IntegerField() 
    order = models.ForeignKey(Order) 
```
[^50]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.79)*

**Verbatim Educational Excerpt** *(None, p.79, lines 1–8)*:
```
Django’s Model-View-Template structure is closely related, as is
Model-View-Controller (MVC). In any case, the aim is to keep the
layers separate (which is a good thing), and to have each layer depend
only on the one below it.
But we want our domain model to have no dependencies whatsoever.
We don’t want infrastructure concerns bleeding over into our domain
model and slowing our unit tests or our ability to make changes.
Instead, as discussed in the introduction, we’ll think of our model as
```
[^51]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.93)*

**Verbatim Educational Excerpt** *(None, p.93, lines 8–15)*:
```
 
    def __init__(self, session): 
        self.session = session 
 
    def add(self, batch): 
        self.session.add(batch) 
 
    def get(self, reference): 
```
[^52]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Duck Typing** *(p.89)*

**Verbatim Educational Excerpt** *(None, p.89, lines 1–8)*:
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
[^53]
**Annotation:** This excerpt demonstrates 'duck typing' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Elif** *(p.107)*

**Verbatim Educational Excerpt** *(None, p.107, lines 15–22)*:
```
            # move it to the correct path 
            elif dest_hash in source_hashes and fn != source_hashes[dest_hash]: 
                shutil.move(dest_path, Path(folder) / source_hashes[dest_hash]) 
 
    # for every file that appears in source but not target, copy the file to 
    # the target 
    for src_hash, fn in source_hashes.items(): 
        if src_hash not in seen: 
```
[^54]
**Annotation:** This excerpt demonstrates 'elif' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 4: Introducing Python Object Types** *(pp.109–140)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^55]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Numeric Types** *(pp.141–175)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^56]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: The Dynamic Typing Interlude** *(pp.176–210)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^57]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 4: Introducing Python Object Types

*Source: None, pages 109–140*

### Chapter Summary
Chapter 4 content. [^58]

### Concept-by-Concept Breakdown
#### **Gil** *(p.126)*

**Verbatim Educational Excerpt** *(None, p.126, lines 13–20)*:
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
[^59]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.134)*

**Verbatim Educational Excerpt** *(None, p.134, lines 2–9)*:
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
[^60]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.133)*

**Verbatim Educational Excerpt** *(None, p.133, lines 13–20)*:
```
 
    def __init__(self, batches): 
        self._batches = set(batches) 
 
    def add(self, batch): 
        self._batches.add(batch) 
 
    def get(self, reference): 
```
[^61]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.129)*

**Verbatim Educational Excerpt** *(None, p.129, lines 12–19)*:
```
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__) 
 
@app.route("/allocate", methods=['POST'])
def allocate_endpoint(): 
    session = get_session() 
    batches = repository.SqlAlchemyRepository(session).list() 
    line = model.OrderLine( 
```
[^62]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.136)*

**Verbatim Educational Excerpt** *(None, p.136, lines 7–14)*:
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
[^63]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.118)*

**Verbatim Educational Excerpt** *(None, p.118, lines 19–24)*:
```
tests verify the interactions between things: did we call
shutil.copy with the right arguments? This coupling
between code and test tends to make tests more brittle, in our
experience.
Overuse of mocks leads to complicated test suites that fail to
explain the code.
```
[^64]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.114)*

**Verbatim Educational Excerpt** *(None, p.114, lines 1–8)*:
```
for sha, filename in dst_hashes.items(): 
        if sha not in src_hashes: 
            yield 'delete', dst_folder / filename
Our tests now act directly on the determine_actions() function:
Nicer-looking tests (test_sync.py)
def test_when_a_file_exists_in_the_source_but_not_the_destination(): 
    src_hashes = {'hash1': 'fn1'} 
    dst_hashes = {} 
```
[^65]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 17 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.130)*

**Verbatim Educational Excerpt** *(None, p.130, lines 15–22)*:
```
    r = requests.post(f'{url}/allocate', json=line1) 
    assert r.status_code == 201 
    assert r.json()['batchref'] == batch1 
 
    # second order should go to batch 2 
    r = requests.post(f'{url}/allocate', json=line2) 
    assert r.status_code == 201 
    assert r.json()['batchref'] == batch2
```
[^66]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.119)*

**Verbatim Educational Excerpt** *(None, p.119, lines 10–17)*:
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
[^67]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.119)*

**Verbatim Educational Excerpt** *(None, p.119, lines 3–10)*:
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
[^68]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.118)*

**Verbatim Educational Excerpt** *(None, p.118, lines 10–17)*:
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
[^69]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.139)*

**Verbatim Educational Excerpt** *(None, p.139, lines 3–10)*:
```
E2E test and a few stub service-layer tests for you to get started on GitHub.
If that’s not enough, continue into the E2E tests and flask_app.py, and refactor the Flask adapter
to be more RESTful. Notice how doing so doesn’t require any change to our service layer or
domain layer!
TIP
If you decide you want to build a read-only endpoint for retrieving allocation info,
just do “the simplest thing that can possibly work,” which is repo.get() right in
the Flask handler. We’ll talk more about reads versus writes in Chapter 12.
```
[^70]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.116)*

**Verbatim Educational Excerpt** *(None, p.116, lines 5–12)*:
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
[^71]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Dictionary** *(p.110)*

**Verbatim Educational Excerpt** *(None, p.110, lines 13–20)*:
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
[^72]
**Annotation:** This excerpt demonstrates 'dictionary' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Duck Typing** *(p.116)*

**Verbatim Educational Excerpt** *(None, p.116, lines 8–15)*:
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
[^73]
**Annotation:** This excerpt demonstrates 'duck typing' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 5: Numeric Types** *(pp.141–175)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^74]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: The Dynamic Typing Interlude** *(pp.176–210)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^75]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: String Fundamentals** *(pp.211–265)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^76]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 5: Numeric Types

*Source: None, pages 141–175*

### Chapter Summary
Chapter 5 content. [^77]

### Concept-by-Concept Breakdown
#### **None** *(p.160)*

**Verbatim Educational Excerpt** *(None, p.160, lines 1–8)*:
```
repo, session = FakeRepository([]), FakeSession() 
    services.add_batch("b1", "AREALSKU", 100, None, repo, session) 
 
    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"): 
        services.allocate("o1", "NONEXISTENTSKU", 10, repo, FakeSession())
This is a really nice place to be in. Our service-layer tests depend on
only the service layer itself, leaving us completely free to refactor the
model as we see fit.
```
[^78]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.172)*

**Verbatim Educational Excerpt** *(None, p.172, lines 6–13)*:
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
[^79]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.171)*

**Verbatim Educational Excerpt** *(None, p.171, lines 1–8)*:
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
[^80]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.141)*

**Verbatim Educational Excerpt** *(None, p.141, lines 1–8)*:
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
[^81]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.164)*

**Verbatim Educational Excerpt** *(None, p.164, lines 5–12)*:
```
pattern.
If the Repository pattern is our abstraction over the idea of persistent
storage, the Unit of Work (UoW) pattern is our abstraction over the
idea of atomic operations. It will allow us to finally and fully
decouple our service layer from the data layer.
Figure 6-1 shows that, currently, a lot of communication occurs across
the layers of our infrastructure: the API talks directly to the database
layer to start a session, it talks to the repository layer to initialize
```
[^82]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.172)*

**Verbatim Educational Excerpt** *(None, p.172, lines 10–17)*:
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
[^83]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.142)*

**Verbatim Educational Excerpt** *(None, p.142, lines 2–9)*:
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
[^84]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 14 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.152)*

**Verbatim Educational Excerpt** *(None, p.152, lines 4–11)*:
```
 
    assert in_stock_batch.available_quantity == 90 
    assert shipment_batch.available_quantity == 100 
 
 
# service-layer test:
def test_prefers_warehouse_batches_to_shipments(): 
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None) 
```
[^85]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.153)*

**Verbatim Educational Excerpt** *(None, p.153, lines 6–13)*:
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
[^86]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.152)*

**Verbatim Educational Excerpt** *(None, p.152, lines 31–33)*:
```
and that orders are still being allocated.
If we accidentally change one of those behaviors, our tests will break.
The flip side, though, is that if we want to change the design of our
```
[^87]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.141)*

**Verbatim Educational Excerpt** *(None, p.141, lines 24–31)*:
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
[^88]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.172)*

**Verbatim Educational Excerpt** *(None, p.172, lines 12–19)*:
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
[^89]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Context Manager** *(p.170)*

**Verbatim Educational Excerpt** *(None, p.170, lines 23–30)*:
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
[^90]
**Annotation:** This excerpt demonstrates 'context manager' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.152)*

**Verbatim Educational Excerpt** *(None, p.152, lines 29–33)*:
```
change while we’re working. We use tests to check that the API
continues to return 200, that the database session continues to commit,
and that orders are still being allocated.
If we accidentally change one of those behaviors, our tests will break.
The flip side, though, is that if we want to change the design of our
```
[^91]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Datetime** *(p.160)*

**Verbatim Educational Excerpt** *(None, p.160, lines 24–27)*:
```
    if eta is not None: 
        eta = datetime.fromisoformat(eta).date() 
    services.add_batch( 
        request.json['ref'], request.json['sku'], request.json['qty'], eta,
```
[^92]
**Annotation:** This excerpt demonstrates 'datetime' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 6: The Dynamic Typing Interlude** *(pp.176–210)*

This later chapter builds upon the concepts introduced here, particularly: None, __enter__, __exit__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^93]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __enter__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: String Fundamentals** *(pp.211–265)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^94]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Lists and Dictionaries** *(pp.266–315)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^95]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 6: The Dynamic Typing Interlude

*Source: None, pages 176–210*

### Chapter Summary
Chapter 6 content. [^96]

### Concept-by-Concept Breakdown
#### **None** *(p.199)*

**Verbatim Educational Excerpt** *(None, p.199, lines 6–13)*:
```
        product = uow.products.get(sku=sku) 
        if product is None: 
            product = model.Product(sku, batches=[]) 
            uow.products.add(product) 
        product.batches.append(model.Batch(ref, sku, qty, eta)) 
        uow.commit() 
 
 
```
[^97]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.177)*

**Verbatim Educational Excerpt** *(None, p.177, lines 1–8)*:
```
def __enter__(self):
        return self
    def __exit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            self.commit()  
        else:
            self.rollback()  
Should we have an implicit commit in the happy path?
```
[^98]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.177)*

**Verbatim Educational Excerpt** *(None, p.177, lines 2–9)*:
```
        return self
    def __exit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            self.commit()  
        else:
            self.rollback()  
Should we have an implicit commit in the happy path?
And roll back only on exception?
```
[^99]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.196)*

**Verbatim Educational Excerpt** *(None, p.196, lines 3–10)*:
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
[^100]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.183)*

**Verbatim Educational Excerpt** *(None, p.183, lines 8–15)*:
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
[^101]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.180)*

**Verbatim Educational Excerpt** *(None, p.180, lines 5–12)*:
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
[^102]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.191)*

**Verbatim Educational Excerpt** *(None, p.191, lines 3–10)*:
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
[^103]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 15 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.208)*

**Verbatim Educational Excerpt** *(None, p.208, lines 28–32)*:
```
    )
    assert version == 2  
    [exception] = exceptions
    assert 'could not serialize access due to concurrent update' in 
str(exception)
```
[^104]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.197)*

**Verbatim Educational Excerpt** *(None, p.197, lines 5–12)*:
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
[^105]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.189)*

**Verbatim Educational Excerpt** *(None, p.189, lines 16–23)*:
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
[^106]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.176)*

**Verbatim Educational Excerpt** *(None, p.176, lines 1–8)*:
```
def test_rolls_back_on_error(session_factory): 
    class MyException(Exception): 
        pass 
 
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory) 
    with pytest.raises(MyException): 
        with uow: 
            insert_batch(uow.session, 'batch1', 'LARGE-FORK', 100, None) 
```
[^107]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.180)*

**Verbatim Educational Excerpt** *(None, p.180, lines 9–16)*:
```
For this chapter, probably the best thing to try is to implement a UoW from scratch. The code, as
always, is on GitHub. You could either follow the model we have quite closely, or perhaps
experiment with separating the UoW (whose responsibilities are commit(), rollback(), and
providing the .batches repository) from the context manager, whose job is to initialize things, and
then do the commit or rollback on exit. If you feel like going all-functional rather than messing
about with all these classes, you could use @contextmanager from contextlib.
We’ve stripped out both the actual UoW and the fakes, as well as paring back the abstract UoW.
Why not send us a link to your repo if you come up with something you’re particularly proud of?
```
[^108]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.191)*

**Verbatim Educational Excerpt** *(None, p.191, lines 9–16)*:
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
[^109]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Constructor** *(p.205)*

**Verbatim Educational Excerpt** *(None, p.205, lines 23–30)*:
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
[^110]
**Annotation:** This excerpt demonstrates 'constructor' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Context Manager** *(p.180)*

**Verbatim Educational Excerpt** *(None, p.180, lines 11–18)*:
```
experiment with separating the UoW (whose responsibilities are commit(), rollback(), and
providing the .batches repository) from the context manager, whose job is to initialize things, and
then do the commit or rollback on exit. If you feel like going all-functional rather than messing
about with all these classes, you could use @contextmanager from contextlib.
We’ve stripped out both the actual UoW and the fakes, as well as paring back the abstract UoW.
Why not send us a link to your repo if you come up with something you’re particularly proud of?
TIP
This is another example of the lesson from Chapter 5: as we build better
```
[^111]
**Annotation:** This excerpt demonstrates 'context manager' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 7: String Fundamentals** *(pp.211–265)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^112]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Lists and Dictionaries** *(pp.266–315)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^113]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Tuples, Files, and Everything Else** *(pp.316–360)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^114]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 7: String Fundamentals

*Source: None, pages 211–265*

### Chapter Summary
Chapter 7 content. [^115]

### Concept-by-Concept Breakdown
#### **None** *(p.259)*

**Verbatim Educational Excerpt** *(None, p.259, lines 26–31)*:
```
         uow = FakeUnitOfWork() 
-        services.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)
+        messagebus.handle(
+            events.BatchCreated("b1", "CRUNCHY-ARMCHAIR", 100, None), uow
+        ) 
         assert uow.products.get("CRUNCHY-ARMCHAIR") is not None
```
[^116]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.239)*

**Verbatim Educational Excerpt** *(None, p.239, lines 13–20)*:
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
[^117]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.230)*

**Verbatim Educational Excerpt** *(None, p.230, lines 10–17)*:
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
[^118]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.234)*

**Verbatim Educational Excerpt** *(None, p.234, lines 25–29)*:
```
not necessarily be Python services. Celery’s API for distributing tasks is essentially “function
name plus arguments,” which is more restrictive, and Python-only.
Option 1: The Service Layer Takes
Events from the Model and Puts Them on
the Message Bus
```
[^119]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.234)*

**Verbatim Educational Excerpt** *(None, p.234, lines 5–12)*:
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
[^120]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 14 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.265)*

**Verbatim Educational Excerpt** *(None, p.265, lines 7–14)*:
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
[^121]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.219)*

**Verbatim Educational Excerpt** *(None, p.219, lines 20–21)*:
```
a system from many small components that interact through
asynchronous message passing.
```
[^122]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.232)*

**Verbatim Educational Excerpt** *(None, p.232, lines 8–15)*:
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
[^123]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.214)*

**Verbatim Educational Excerpt** *(None, p.214, lines 7–13)*:
```
to a group of related objects. It’s the aggregate’s job to check that the objects within its remit
are consistent with each other and with our rules, and to reject changes that would break the
rules.
Aggregates and concurrency issues go together
When thinking about implementing these consistency checks, we end up thinking about
transactions and locks. Choosing the right aggregate is about performance as well as
conceptual organization of your domain.
```
[^124]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.231)*

**Verbatim Educational Excerpt** *(None, p.231, lines 8–15)*:
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
[^125]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.218)*

**Verbatim Educational Excerpt** *(None, p.218, lines 14–21)*:
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
[^126]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.239)*

**Verbatim Educational Excerpt** *(None, p.239, lines 1–8)*:
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
[^127]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.228)*

**Verbatim Educational Excerpt** *(None, p.228, lines 9–16)*:
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
[^128]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.233)*

**Verbatim Educational Excerpt** *(None, p.233, lines 1–8)*:
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
[^129]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.233)*

**Verbatim Educational Excerpt** *(None, p.233, lines 1–8)*:
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
[^130]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 8: Lists and Dictionaries** *(pp.266–315)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^131]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Tuples, Files, and Everything Else** *(pp.316–360)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^132]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: Introducing Python Statements** *(pp.361–395)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^133]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 8: Lists and Dictionaries

*Source: None, pages 266–315*

### Chapter Summary
Chapter 8 content. [^134]

### Concept-by-Concept Breakdown
#### **None** *(p.267)*

**Verbatim Educational Excerpt** *(None, p.267, lines 28–35)*:
```
    def _get(self, sku): 
        return next((p for p in self._products if p.sku == sku), None) 
 
    def _get_by_batchref(self, batchref): 
        return next(( 
            p for p in self._products for b in p.batches 
            if b.reference == batchref 
        ), None)
```
[^135]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.270)*

**Verbatim Educational Excerpt** *(None, p.270, lines 7–14)*:
```
 
    def __init__(self): 
        super().__init__() 
        self.events_published = []  # type: List[events.Event] 
 
    def publish_events(self): 
        for product in self.products.seen: 
            while product.events: 
```
[^136]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.290)*

**Verbatim Educational Excerpt** *(None, p.290, lines 18–25)*:
```
can be subtle. Expect 
bikeshedding arguments over the 
differences.
We’re expressly inviting failure. 
We know that sometimes things 
will break, and 
we’re choosing to handle that by 
making the failures smaller and 
```
[^137]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.298)*

**Verbatim Educational Excerpt** *(None, p.298, lines 1–8)*:
```
Figure 11-5. Command flow with error
CONNASCENCE
We’re using the term coupling here, but there’s another way to describe the relationships
between our systems. Connascence is a term used by some authors to describe the different
types of coupling.
Connascence isn’t bad, but some types of connascence are stronger than others. We want to
have strong connascence locally, as when two classes are closely related, but weak
connascence at a distance.
```
[^138]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 14 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.271)*

**Verbatim Educational Excerpt** *(None, p.271, lines 5–12)*:
```
    [batch1, batch2] = uow.products.get(sku="INDIFFERENT-TABLE").batches 
    assert batch1.available_quantity == 10 
    assert batch2.available_quantity == 50 
 
    messagebus.handle(events.BatchQuantityChanged("batch1", 25), uow) 
 
    # assert on new events emitted rather than downstream side-effects 
    [reallocation_event] = uow.events_published 
```
[^139]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.299)*

**Verbatim Educational Excerpt** *(None, p.299, lines 1–8)*:
```
The Alternative: Temporal Decoupling
Using Asynchronous Messaging
How do we get appropriate coupling? We’ve already seen part of the
answer, which is that we should think in terms of verbs, not nouns. Our
domain model is about modeling a business process. It’s not a static
data model about a thing; it’s a model of a verb.
So instead of thinking about a system for orders and a system for
batches, we think about a system for ordering and a system for
```
[^140]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.290)*

**Verbatim Educational Excerpt** *(None, p.290, lines 22–29)*:
```
We know that sometimes things 
will break, and 
we’re choosing to handle that by 
making the failures smaller and 
more isolated. 
This can make the system harder 
to reason about and requires 
better monitoring.
```
[^141]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.278)*

**Verbatim Educational Excerpt** *(None, p.278, lines 14–21)*:
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
[^142]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.298)*

**Verbatim Educational Excerpt** *(None, p.298, lines 6–13)*:
```
Connascence isn’t bad, but some types of connascence are stronger than others. We want to
have strong connascence locally, as when two classes are closely related, but weak
connascence at a distance.
In our first example of a distributed ball of mud, we see Connascence of Execution: multiple
components need to know the correct order of work for an operation to be successful.
When thinking about error conditions here, we’re talking about Connascence of Timing: multiple
things have to happen, one after another, for the operation to work.
When we replace our RPC-style system with events, we replace both of these types of
```
[^143]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.280)*

**Verbatim Educational Excerpt** *(None, p.280, lines 17–24)*:
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
[^144]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.267)*

**Verbatim Educational Excerpt** *(None, p.267, lines 1–8)*:
```
def _add(self, product: model.Product): 
        raise NotImplementedError 
 
    @abc.abstractmethod 
    def _get(self, sku) -> model.Product: 
        raise NotImplementedError 
 
    @abc.abstractmethod 
```
[^145]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Elif** *(p.279)*

**Verbatim Educational Excerpt** *(None, p.279, lines 18–25)*:
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
[^146]
**Annotation:** This excerpt demonstrates 'elif' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.279)*

**Verbatim Educational Excerpt** *(None, p.279, lines 21–26)*:
```
            results.append(cmd_result)
        else:
            raise Exception(f'{message} was not an Event or Command')
    return results
It still has a main handle() entrypoint that takes a message, which
may be a command or an event.
```
[^147]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Error Handling** *(p.278)*

**Verbatim Educational Excerpt** *(None, p.278, lines 6–13)*:
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
[^148]
**Annotation:** This excerpt demonstrates 'error handling' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.280)*

**Verbatim Educational Excerpt** *(None, p.280, lines 15–22)*:
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
[^149]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 9: Tuples, Files, and Everything Else** *(pp.316–360)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^150]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: Introducing Python Statements** *(pp.361–395)*

This later chapter builds upon the concepts introduced here, particularly: None, argument, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^151]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, argument appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Assignments, Expressions, and Prints** *(pp.396–435)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^152]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 9: Tuples, Files, and Everything Else

*Source: None, pages 316–360*

### Chapter Summary
Chapter 9 content. [^153]

### Concept-by-Concept Breakdown
#### **None** *(p.355)*

**Verbatim Educational Excerpt** *(None, p.355, lines 12–19)*:
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
[^154]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.340)*

**Verbatim Educational Excerpt** *(None, p.340, lines 4–11)*:
```
 
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY): 
        self.session_factory = session_factory 
        ...
We take advantage of it in our integration tests to be able to sometimes
use SQLite instead of Postgres:
Integration tests against a different DB
(tests/integration/test_uow.py)
```
[^155]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.354)*

**Verbatim Educational Excerpt** *(None, p.354, lines 11–18)*:
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
[^156]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.319)*

**Verbatim Educational Excerpt** *(None, p.319, lines 5–12)*:
```
And what about the Repository pattern? Isn’t that meant to be our
abstraction around the database? Why don’t we reuse that?
Well, let’s explore that seemingly simpler alternative first, and see
what it looks like in practice.
We’ll still keep our view in a separate views.py module; enforcing a
clear distinction between reads and writes in your application is still a
good idea. We apply command-query separation, and it’s easy to see
which code modifies state (the event handlers) and which code just
```
[^157]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.355)*

**Verbatim Educational Excerpt** *(None, p.355, lines 12–19)*:
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
[^158]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.349)*

**Verbatim Educational Excerpt** *(None, p.349, lines 5–12)*:
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
[^159]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.347)*

**Verbatim Educational Excerpt** *(None, p.347, lines 1–8)*:
```
DI using classes
# we replace the old `def allocate(cmd, uow)` with:
class AllocateHandler:
    def __init__(self, uow: unit_of_work.AbstractUnitOfWork):  
        self.uow = uow
    def __call__(self, cmd: commands.Allocate):  
        line = OrderLine(cmd.orderid, cmd.sku, cmd.qty)
        with self.uow:
```
[^160]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.317)*

**Verbatim Educational Excerpt** *(None, p.317, lines 11–18)*:
```
    r = api_client.post_to_allocate(orderid, sku, qty=3) 
    assert r.status_code == 202 
 
    r = api_client.get_allocation(orderid) 
    assert r.ok 
    assert r.json() == [ 
        {'sku': sku, 'batchref': earlybatch}, 
    ] 
```
[^161]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.332)*

**Verbatim Educational Excerpt** *(None, p.332, lines 1–8)*:
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
[^162]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.324)*

**Verbatim Educational Excerpt** *(None, p.324, lines 6–13)*:
```
needs, and then issue individual queries for each object to retrieve
their attributes. This is especially likely if there are any foreign-key
relationships on your objects.
NOTE
In all fairness, we should say that SQLAlchemy is quite good at avoiding the
SELECT N+1 problem. It doesn’t display it in the preceding example, and you can
request eager loading explicitly to avoid it when dealing with joined objects.
Beyond SELECT N+1, you may have other reasons for wanting to
```
[^163]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.330)*

**Verbatim Educational Excerpt** *(None, p.330, lines 5–12)*:
```
REBUILDING FROM SCRATCH
“What happens when it breaks?” should be the first question we ask as engineers.
How do we deal with a view model that hasn’t been updated because of a bug or temporary
outage? Well, this is just another case where events and commands can fail independently.
If we never updated the view model, and the ASYMMETRICAL-DRESSER was forever in stock, that
would be annoying for customers, but the allocate service would still fail, and we’d take action to
fix the problem.
Rebuilding a view model is easy, though. Since we’re using a service layer to update our view
```
[^164]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.347)*

**Verbatim Educational Excerpt** *(None, p.347, lines 1–8)*:
```
DI using classes
# we replace the old `def allocate(cmd, uow)` with:
class AllocateHandler:
    def __init__(self, uow: unit_of_work.AbstractUnitOfWork):  
        self.uow = uow
    def __call__(self, cmd: commands.Allocate):  
        line = OrderLine(cmd.orderid, cmd.sku, cmd.qty)
        with self.uow:
```
[^165]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.322)*

**Verbatim Educational Excerpt** *(None, p.322, lines 16–21)*:
```
pattern. If you’re building a simple CRUD app, reads and writes are going to be
closely related, so you don’t need a domain model or CQRS. But the more
complex your domain, the more likely you are to need both.
To make a facile point, your domain classes will have multiple
methods for modifying state, and you won’t need any of them for read-
only operations.
```
[^166]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Closure** *(p.345)*

**Verbatim Educational Excerpt** *(None, p.345, lines 2–9)*:
```
Preparing Handlers: Manual DI with
Closures and Partials
One way to turn a function with dependencies into one that’s ready to
be called later with those dependencies already injected is to use
closures or partial functions to compose the function with its
dependencies:
Examples of DI using closures or partial functions
# existing allocate function, with abstract uow dependency
```
[^167]
**Annotation:** This excerpt demonstrates 'closure' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Comprehension** *(p.321)*

**Verbatim Educational Excerpt** *(None, p.321, lines 9–16)*:
```
Now we have products but we actually want batch references, so
we get all the possible batches with a list comprehension.
We filter again to get just the batches for our specific order. That,
in turn, relies on our Batch objects being able to tell us which
order IDs it has allocated.
We implement that last using a .orderid property:
An arguably unnecessary property on our model
(src/allocation/domain/model.py)
```
[^168]
**Annotation:** This excerpt demonstrates 'comprehension' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 10: Introducing Python Statements** *(pp.361–395)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, args.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^169]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Assignments, Expressions, and Prints** *(pp.396–435)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^170]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 12: if Tests and Syntax Rules** *(pp.436–465)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^171]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 10: Introducing Python Statements

*Source: None, pages 361–395*

### Chapter Summary
Chapter 10 content. [^172]

### Concept-by-Concept Breakdown
#### **None** *(p.361)*

**Verbatim Educational Excerpt** *(None, p.361, lines 9–16)*:
```
        notifications=notifications.EmailNotifications(),  
        publish=lambda *args: None,
    )
    yield bus
    clear_mappers()
def get_email_from_mailhog(sku):  
    host, port = map(config.get_email_host_and_port().get, ['host', 
'http_port'])
```
[^173]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.394)*

**Verbatim Educational Excerpt** *(None, p.394, lines 39–46)*:
```
work
Abstraction around data integrity. Each unit 
of work represents an atomic update. Makes 
repositories available. Tracks new events on 
retrieved aggregates.
Message 
bus 
(internal)
```
[^174]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.361)*

**Verbatim Educational Excerpt** *(None, p.361, lines 9–16)*:
```
        notifications=notifications.EmailNotifications(),  
        publish=lambda *args: None,
    )
    yield bus
    clear_mappers()
def get_email_from_mailhog(sku):  
    host, port = map(config.get_email_host_and_port().get, ['host', 
'http_port'])
```
[^175]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.366)*

**Verbatim Educational Excerpt** *(None, p.366, lines 12–19)*:
```
to technical debt and refactoring, so long as engineers can make a
reasoned argument for fixing things.
TIP
Making complex changes to a system is often an easier sell if you link it to feature
work. Perhaps you’re launching a new product or opening your service to new
markets? This is the right time to spend engineering resources on fixing the
foundations. With a six-month project to deliver, it’s easier to make the argument
for three weeks of cleanup work. Bob refers to this as architecture tax.
```
[^176]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.383)*

**Verbatim Educational Excerpt** *(None, p.383, lines 1–8)*:
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
[^177]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 26 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.361)*

**Verbatim Educational Excerpt** *(None, p.361, lines 23–29)*:
```
    email = get_email_from_mailhog(sku)
    assert email['Raw']['From'] == 'allocations@example.com'  
    assert email['Raw']['To'] == ['stock@made.com']
    assert f'Out of stock for {sku}' in email['Raw']['Data']
We use our bootstrapper to build a message bus that talks to the
real notifications class.
We figure out how to fetch emails from our “real” email server.
```
[^178]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.378)*

**Verbatim Educational Excerpt** *(None, p.378, lines 1–8)*:
```
Figure E-3. After: loose coupling with asynchronous events (you can find a high-
resolution version of this diagram at cosmicpython.com)
Practically, this was a several month-long project. Our first step was
to write a domain model that could represent batches, shipments, and
products. We used TDD to build a toy system that could answer a
single question: “If I want N units of HAZARDOUS_RUG, how long
will they take to be delivered?”
TIP
```
[^179]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.394)*

**Verbatim Educational Excerpt** *(None, p.394, lines 10–17)*:
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
[^180]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.367)*

**Verbatim Educational Excerpt** *(None, p.367, lines 5–12)*:
```
Figure E-1. Domain of a collaboration system
This was the system in which Bob first learned how to break apart a
ball of mud, and it was a doozy. There was logic everywhere—in the
web pages, in manager objects, in helpers, in fat service classes that
we’d written to abstract the managers and helpers, and in hairy
command objects that we’d written to break apart the services.
If you’re working in a system that’s reached this point, the situation can
feel hopeless, but it’s never too late to start weeding an overgrown
```
[^181]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.361)*

**Verbatim Educational Excerpt** *(None, p.361, lines 1–8)*:
```
In our integration tests, we use the real EmailNotifications class,
talking to the MailHog server in the Docker cluster:
Integration test for email (tests/integration/test_email.py)
@pytest.fixture
def bus(sqlite_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=True,
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),
```
[^182]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.373)*

**Verbatim Educational Excerpt** *(None, p.373, lines 7–14)*:
```
        workspace.archive()
Or even recurse over collections of folders and documents:
def lock_documents_in_folder(folder): 
 
    for doc in folder.documents: 
         doc.archive() 
 
     for child in folder.children: 
```
[^183]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.394)*

**Verbatim Educational Excerpt** *(None, p.394, lines 7–14)*:
```
Domain
Defines the business 
logic.
Entity
A domain object whose attributes may 
change but that has a recognizable identity 
over time.
Value 
```
[^184]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.383)*

**Verbatim Educational Excerpt** *(None, p.383, lines 28–35)*:
```
to use, perhaps in an initially limited and imperfect fashion. You may discover, as I did, that the
first problem you pick might be a bit too difficult; if so, move on to something else. Don’t try to boil
the ocean, and don’t be too afraid of making mistakes. It will be a learning experience, and you
can be confident that you’re moving roughly in a direction that others have found useful.
So, if you’re feeling the pain too, give these ideas a try. Don’t feel you need permission to
rearchitect everything. Just look for somewhere small to start. And above all, do it to solve a
specific problem. If you’re successful in solving it, you’ll know you got something right—and
others will too.
```
[^185]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Error Handling** *(p.371)*

**Verbatim Educational Excerpt** *(None, p.371, lines 7–14)*:
```
These use-case functions will mostly be about logging, data access,
and error handling. Once you’ve done this step, you’ll have a grasp of
what your program actually does, and a way to make sure each
operation has a clearly defined start and finish. We’ll have taken a step
toward building a pure domain model.
Read Working Effectively with Legacy Code by Michael C. Feathers
(Prentice Hall) for guidance on getting legacy code under test and
starting separating responsibilities.
```
[^186]
**Annotation:** This excerpt demonstrates 'error handling' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.370)*

**Verbatim Educational Excerpt** *(None, p.370, lines 2–9)*:
```
Many years ago, Bob worked for a software company that had outsourced the first version of its
application, an online collaboration platform for sharing and working on files.
When the company brought development in-house, it passed through several generations of
developers’ hands, and each wave of new developers added more complexity to the code’s
structure.
At its heart, the system was an ASP.NET Web Forms application, built with an NHibernate ORM.
Users would upload documents into workspaces, where they could invite other workspace
members to review, comment on, or modify their work.
```
[^187]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 11: Assignments, Expressions, and Prints** *(pp.396–435)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, args.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^188]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 12: if Tests and Syntax Rules** *(pp.436–465)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^189]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 13: while and for Loops** *(pp.466–500)*

This later chapter builds upon the concepts introduced here, particularly: abstraction, argument, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^190]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts abstraction, argument appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 11: Assignments, Expressions, and Prints

*Source: None, pages 396–435*

### Chapter Summary
Chapter 11 content. [^191]

### Concept-by-Concept Breakdown
#### **None** *(p.417)*

**Verbatim Educational Excerpt** *(None, p.417, lines 12–19)*:
```
    d_b1 = django_models.Batch.objects.create( 
    reference="batch1", sku=sku, qty=100, eta=None
) 
    d_b2 = django_models.Batch.objects.create( 
    reference="batch2", sku=sku, qty=100, eta=None
) 
    django_models.Allocation.objects.create(line=d_line, batch=d_batch1) 
 
```
[^192]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.421)*

**Verbatim Educational Excerpt** *(None, p.421, lines 15–22)*:
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
[^193]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Eq__** *(p.417)*

**Verbatim Educational Excerpt** *(None, p.417, lines 23–30)*:
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
[^194]
**Annotation:** This excerpt demonstrates '__eq__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.421)*

**Verbatim Educational Excerpt** *(None, p.421, lines 19–26)*:
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
[^195]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.415)*

**Verbatim Educational Excerpt** *(None, p.415, lines 8–15)*:
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
[^196]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.410)*

**Verbatim Educational Excerpt** *(None, p.410, lines 1–8)*:
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
[^197]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.410)*

**Verbatim Educational Excerpt** *(None, p.410, lines 1–8)*:
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
[^198]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.411)*

**Verbatim Educational Excerpt** *(None, p.411, lines 11–18)*:
```
All we need to do (“all we need to do”) is reimplement those same
abstractions, but with CSVs underlying them instead of a database.
And as you’ll see, it really is relatively straightforward.
Implementing a Repository and Unit of
Work for CSVs
Here’s what a CSV-based repository could look like. It abstracts away
all the logic for reading CSVs from disk, including the fact that it has
to read two different CSVs (one for batches and one for allocations),
```
[^199]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.421)*

**Verbatim Educational Excerpt** *(None, p.421, lines 19–26)*:
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
[^200]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.417)*

**Verbatim Educational Excerpt** *(None, p.417, lines 1–8)*:
```
assert saved_batch.qty == batch._purchased_quantity 
    assert saved_batch.eta == batch.eta
The second test is a bit more involved since it has allocations, but it is
still made up of familiar-looking Django code:
Second repository test is more involved
(tests/integration/test_repository.py)
@pytest.mark.django_db
def test_repository_can_retrieve_a_batch_with_allocations(): 
```
[^201]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 11 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.417)*

**Verbatim Educational Excerpt** *(None, p.417, lines 1–8)*:
```
assert saved_batch.qty == batch._purchased_quantity 
    assert saved_batch.eta == batch.eta
The second test is a bit more involved since it has allocations, but it is
still made up of familiar-looking Django code:
Second repository test is more involved
(tests/integration/test_repository.py)
@pytest.mark.django_db
def test_repository_can_retrieve_a_batch_with_allocations(): 
```
[^202]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.434)*

**Verbatim Educational Excerpt** *(None, p.434, lines 15–22)*:
```
    return e.code, 400
And here’s how we might plug it in to our asynchronous message
processor:
Validation errors when handling Redis messages
(src/allocation/redis_pubsub.py)
def handle_change_batch_quantity(m, bus: messagebus.MessageBus): 
    try: 
        bus.handle_message('ChangeBatchQuantity', m) 
```
[^203]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Bytecode** *(p.400)*

**Verbatim Educational Excerpt** *(None, p.400, lines 26–29)*:
```
      - API_HOST=app
      - PYTHONDONTWRITEBYTECODE=1  
    volumes:  
5
```
[^204]
**Annotation:** This excerpt demonstrates 'bytecode' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.430)*

**Verbatim Educational Excerpt** *(None, p.430, lines 12–19)*:
```
name of the field and the value is the parser.
We use the make_dataclass function from the dataclass module to
dynamically create our message type.
We patch the from_json method onto our dynamic dataclass.
We can create reusable parsers for quantity, SKU, and so on to
keep things DRY.
Declaring a message type becomes a one-liner.
This comes at the expense of losing the types on your dataclass, so
```
[^205]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.427)*

**Verbatim Educational Excerpt** *(None, p.427, lines 14–19)*:
```
valid, and inputs that don’t are invalid.
If the input is invalid, the operation can’t continue but should exit with
some kind of error. In other words, validation is about creating
preconditions. We find it useful to separate our preconditions into
three subtypes: syntax, semantics, and pragmatics.
Validating Syntax
```
[^206]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 12: if Tests and Syntax Rules** *(pp.436–465)*

This later chapter builds upon the concepts introduced here, particularly: None, __enter__, __eq__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^207]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __enter__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 13: while and for Loops** *(pp.466–500)*

This later chapter builds upon the concepts introduced here, particularly: __enter__, __eq__, __exit__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^208]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts __enter__, __eq__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 12: if Tests and Syntax Rules

*Source: None, pages 436–465*

### Chapter Summary
Chapter 12 content. [^209]

### Concept-by-Concept Breakdown
#### **None** *(p.436)*

**Verbatim Educational Excerpt** *(None, p.436, lines 17–24)*:
```
    product = uow.products.get(event.sku)
    if product is None:
        raise ProductNotFound(event)
We use a common base class for errors that mean a message is
invalid.
Using a specific error type for this problem makes it easier to
report on and handle the error. For example, it’s easy to map
ProductNotFound to a 404 in Flask.
```
[^210]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.460)*

**Verbatim Educational Excerpt** *(None, p.460, lines 12–19)*:
```
replacement with unit tests, Why Not Just Patch It Out?
__enter__ and __exit__ magic methods, Unit of Work and Its Context
Manager, The Real Unit of Work Uses SQLAlchemy Sessions
entities
defined, Value Objects and Entities
identity equality, Value Objects and Entities
value objects versus, Exceptions Can Express Domain Concepts
Too
```
[^211]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Eq__** *(p.460)*

**Verbatim Educational Excerpt** *(None, p.460, lines 20–24)*:
```
entrypoints, Putting Things in Folders to See Where It All Belongs
__eq__magic method, Value Objects and Entities
equality operators, implementing on entities, Value Objects and
Entities
error handling
```
[^212]
**Annotation:** This excerpt demonstrates '__eq__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.460)*

**Verbatim Educational Excerpt** *(None, p.460, lines 12–19)*:
```
replacement with unit tests, Why Not Just Patch It Out?
__enter__ and __exit__ magic methods, Unit of Work and Its Context
Manager, The Real Unit of Work Uses SQLAlchemy Sessions
entities
defined, Value Objects and Entities
identity equality, Value Objects and Entities
value objects versus, Exceptions Can Express Domain Concepts
Too
```
[^213]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.436)*

**Verbatim Educational Excerpt** *(None, p.436, lines 5–12)*:
```
class MessageUnprocessable(Exception):  
    def __init__(self, message):
        self.message = message
class ProductNotFound(MessageUnprocessable):  
   """" 
   This exception is raised when we try to perform an action on a product 
   that doesn't exist in our database. 
   """"
```
[^214]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.442)*

**Verbatim Educational Excerpt** *(None, p.442, lines 1–8)*:
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
[^215]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.436)*

**Verbatim Educational Excerpt** *(None, p.436, lines 4–11)*:
```
"""
class MessageUnprocessable(Exception):  
    def __init__(self, message):
        self.message = message
class ProductNotFound(MessageUnprocessable):  
   """" 
   This exception is raised when we try to perform an action on a product 
   that doesn't exist in our database. 
```
[^216]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.452)*

**Verbatim Educational Excerpt** *(None, p.452, lines 1–8)*:
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
[^217]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.436)*

**Verbatim Educational Excerpt** *(None, p.436, lines 4–11)*:
```
"""
class MessageUnprocessable(Exception):  
    def __init__(self, message):
        self.message = message
class ProductNotFound(MessageUnprocessable):  
   """" 
   This exception is raised when we try to perform an action on a product 
   that doesn't exist in our database. 
```
[^218]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Closure** *(p.448)*

**Verbatim Educational Excerpt** *(None, p.448, lines 2–9)*:
```
Model
closures
dependency injection using, Preparing Handlers: Manual DI with
Closures and Partials
difference from partial functions, Preparing Handlers: Manual DI
with Closures and Partials
cohesion, high, between coupled elements, A Brief Interlude: On
Coupling and Abstractions
```
[^219]
**Annotation:** This excerpt demonstrates 'closure' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.448)*

**Verbatim Educational Excerpt** *(None, p.448, lines 10–17)*:
```
collaborators, The Unit of Work Collaborates with the Repository
collections, What Is an Aggregate?
Command Handler pattern, Wrap-Up
command-query responsibility segregation (CQRS), Command-Query
Responsibility Segregation (CQRS)-Wrap-Up
building read-only views into our data, Hold On to Your Lunch,
Folks
changing read model implementation to use Redis, Changing Our
```
[^220]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Context Manager** *(p.452)*

**Verbatim Educational Excerpt** *(None, p.452, lines 4–11)*:
```
constraints, Invariants, Constraints, and Consistency
context manager, Unit of Work Pattern
starting Unit of Work as, The Unit of Work Collaborates with the
Repository
Unit of Work and, Unit of Work and Its Context Manager-Fake
Unit of Work for Testing
control flow, using exceptions for, The Model Raises Events
coupling, A Brief Interlude: On Coupling and Abstractions
```
[^221]
**Annotation:** This excerpt demonstrates 'context manager' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.437)*

**Verbatim Educational Excerpt** *(None, p.437, lines 17–24)*:
```
If we get asked to create a batch that already exists, we’ll log a
warning and continue to the next message:
Raise SkipMessage exception for ignorable events
(src/allocation/services.py)
class SkipMessage (Exception): 
    """"
    This exception is raised when a message can't be processed, but there's no
    incorrect behavior. For example, we might receive the same message multiple
```
[^222]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.453)*

**Verbatim Educational Excerpt** *(None, p.453, lines 6–13)*:
```
CRUD wrapper around a database, Part I Recap
CSV over SMTP architecture, Why Not Just Run Everything in a
Spreadsheet?
CSVs, doing everything with, Swapping Out the Infrastructure: Do
Everything with CSVs-Implementing a Repository and Unit of Work
for CSVs
D
data access, applying dependency inversion principle to, Applying the
```
[^223]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.436)*

**Verbatim Educational Excerpt** *(None, p.436, lines 5–12)*:
```
class MessageUnprocessable(Exception):  
    def __init__(self, message):
        self.message = message
class ProductNotFound(MessageUnprocessable):  
   """" 
   This exception is raised when we try to perform an action on a product 
   that doesn't exist in our database. 
   """"
```
[^224]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 13: while and for Loops** *(pp.466–500)*

This later chapter builds upon the concepts introduced here, particularly: __enter__, __eq__, __exit__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the later material.

[^225]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts __enter__, __eq__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 13: while and for Loops

*Source: None, pages 466–500*

### Chapter Summary
Chapter 13 content. [^226]

### Concept-by-Concept Breakdown
#### **__Enter__** *(p.470)*

**Verbatim Educational Excerpt** *(None, p.470, lines 10–17)*:
```
Magic Methods Let Us Use Our Models with Idiomatic Python
__enter__ and __exit__, Unit of Work and Its Context Manager
__eq__, Value Objects and Entities
__hash__, Value Objects and Entities
MagicMock objects, Why Not Just Patch It Out?
mappers, Inverting the Dependency: ORM Depends on Model
message brokers, Using a Redis Pub/Sub Channel for Integration
message bus
```
[^227]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Eq__** *(p.470)*

**Verbatim Educational Excerpt** *(None, p.470, lines 11–18)*:
```
__enter__ and __exit__, Unit of Work and Its Context Manager
__eq__, Value Objects and Entities
__hash__, Value Objects and Entities
MagicMock objects, Why Not Just Patch It Out?
mappers, Inverting the Dependency: ORM Depends on Model
message brokers, Using a Redis Pub/Sub Channel for Integration
message bus
abstract message bus and its real and fake versions, Optionally:
```
[^228]
**Annotation:** This excerpt demonstrates '__eq__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.470)*

**Verbatim Educational Excerpt** *(None, p.470, lines 10–17)*:
```
Magic Methods Let Us Use Our Models with Idiomatic Python
__enter__ and __exit__, Unit of Work and Its Context Manager
__eq__, Value Objects and Entities
__hash__, Value Objects and Entities
MagicMock objects, Why Not Just Patch It Out?
mappers, Inverting the Dependency: ORM Depends on Model
message brokers, Using a Redis Pub/Sub Channel for Integration
message bus
```
[^229]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.468)*

**Verbatim Educational Excerpt** *(None, p.468, lines 6–13)*:
```
hashing a file, Abstracting State Aids Testability
dictionary of hashes to paths, Choosing the Right Abstraction(s)
hoisting I/O, Why Not Just Patch It Out?
I
I/O
disentangling details from program logic, Implementing Our
Chosen Abstractions
domain logic tightly coupled to, Abstracting State Aids
```
[^230]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.478)*

**Verbatim Educational Excerpt** *(None, p.478, lines 20–24)*:
```
This All So Hard?
session argument, Inverting the Dependency: ORM Depends on
Model
Q
queries, Command-Query Responsibility Segregation (CQRS)
```
[^231]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.483)*

**Verbatim Educational Excerpt** *(None, p.483, lines 4–11)*:
```
to the Service Layer?
reasons for, Should Domain Layer Tests Move to the
Service Layer?
end-to-end test of allocate API, testing happy and unhappy paths,
A Typical Service Function
error conditions requiring database checks in Flask app, Error
Conditions That Require Database Checks
first cut of Flask app, The Straightforward Implementation-The
```
[^232]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.473)*

**Verbatim Educational Excerpt** *(None, p.473, lines 2–9)*:
```
Distributed Systems-The Alternative: Temporal Decoupling
Using Asynchronous Messaging
temporal decoupling using asynchronous messaging, The
Alternative: Temporal Decoupling Using Asynchronous
Messaging
testing with end-to-end test, Test-Driving It All Using an
End-to-End Test-Internal Versus External Events
trade-offs, Wrap-Up
```
[^233]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.493)*

**Verbatim Educational Excerpt** *(None, p.493, lines 10–17)*:
```
value objects
defined, Dataclasses Are Great for Value Objects
and entities, Value Objects and Entities
entities versus, Exceptions Can Express Domain Concepts Too
math with, Dataclasses Are Great for Value Objects
using dataclasses for, Dataclasses Are Great for Value Objects
Vens, Rob, Wrap-Up
Vernon, Vaughn, Wrap-Up
```
[^234]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Closure** *(p.475)*

**Verbatim Educational Excerpt** *(None, p.475, lines 19–24)*:
```
dependency injection with, Preparing Handlers: Manual DI with
Closures and Partials
difference from closures, Preparing Handlers: Manual DI with
Closures and Partials
manually creating inline, A Bootstrap Script
patterns, deciding whether you need to use them, Part I Recap
```
[^235]
**Annotation:** This excerpt demonstrates 'closure' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Context Manager** *(p.491)*

**Verbatim Educational Excerpt** *(None, p.491, lines 2–9)*:
```
Pattern-Wrap-Up
and its context manager, Unit of Work and Its Context Manager
fake UoW for testing, Fake Unit of Work for Testing
real UoW using SQLAlchemy session, The Real Unit of
Work Uses SQLAlchemy Sessions
benefits of using, Wrap-Up
collaboration with repository, The Unit of Work Collaborates
with the Repository
```
[^236]
**Annotation:** This excerpt demonstrates 'context manager' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.496)*

**Verbatim Educational Excerpt** *(None, p.496, lines 12–19)*:
```
The markings on a Burmese python begin with an arrow-shaped spot of
light brown on top of the head and continue along the body in
rectangles that stand out against its otherwise tan scales. Before they
reach their full size, which takes two to three years, Burmese pythons
live in trees hunting small mammals and birds. They also swim for
long stretches of time—going up to 30 minutes without air.
Because of habitat destruction, the Burmese python has a conservation
status of Vulnerable. Many of the animals on O’Reilly’s covers are
```
[^237]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.479)*

**Verbatim Educational Excerpt** *(None, p.479, lines 23–25)*:
```
Lunch, Folks
CSV-based repository, Implementing a Repository and Unit of
Work for CSVs
```
[^238]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.471)*

**Verbatim Educational Excerpt** *(None, p.471, lines 6–13)*:
```
Is Given Handlers at Runtime
getting custom with overridden bootstrap defaults, Initializing DI
in Our Tests
handler publishing outgoing event, Our New Outgoing Event
handle_event method, Recovering from Errors Synchronously
handle_event with retries, Recovering from Errors Synchronously
mapping events to handlers, The Message Bus Maps Events to
Handlers
```
[^239]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Dictionary** *(p.468)*

**Verbatim Educational Excerpt** *(None, p.468, lines 6–13)*:
```
hashing a file, Abstracting State Aids Testability
dictionary of hashes to paths, Choosing the Right Abstraction(s)
hoisting I/O, Why Not Just Patch It Out?
I
I/O
disentangling details from program logic, Implementing Our
Chosen Abstractions
domain logic tightly coupled to, Abstracting State Aids
```
[^240]
**Annotation:** This excerpt demonstrates 'dictionary' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Duck Typing** *(p.478)*

**Verbatim Educational Excerpt** *(None, p.478, lines 4–11)*:
```
Up
protocols, abstract base classes, duck typing, and, The Repository in
the Abstract
publish-subscribe system
message bus as
handlers subscribed to receive events, The Message Bus
Maps Events to Handlers
publishing step, Option 1: The Service Layer Takes Events
```
[^241]
**Annotation:** This excerpt demonstrates 'duck typing' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 14: Iterations and Comprehensions

*Source: None, pages 501–540*

### Chapter Summary
Chapter 14 content. [^242]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 15: The Documentation Interlude

*Source: None, pages 541–565*

### Chapter Summary
Chapter 15 content. [^243]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 16: Function Basics

*Source: None, pages 566–600*

### Chapter Summary
Chapter 16 content. [^244]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 17: Scopes

*Source: None, pages 601–635*

### Chapter Summary
Chapter 17 content. [^245]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 18: Arguments

*Source: None, pages 636–680*

### Chapter Summary
Chapter 18 content. [^246]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 19: Advanced Function Topics

*Source: None, pages 681–720*

### Chapter Summary
Chapter 19 content. [^247]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 20: Comprehensions and Generations

*Source: None, pages 721–755*

### Chapter Summary
Chapter 20 content. [^248]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 21: Modules: The Big Picture

*Source: None, pages 756–785*

### Chapter Summary
Chapter 21 content. [^249]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 22: Module Coding Basics

*Source: None, pages 786–820*

### Chapter Summary
Chapter 22 content. [^250]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 23: Module Packages

*Source: None, pages 821–850*

### Chapter Summary
Chapter 23 content. [^251]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 24: Advanced Module Topics

*Source: None, pages 851–885*

### Chapter Summary
Chapter 24 content. [^252]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 25: Debugging and Testing

*Source: None, pages 886–920*

### Chapter Summary
Chapter 25 content. [^253]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 26: OOP: The Big Picture

*Source: None, pages 921–945*

### Chapter Summary
Chapter 26 content. [^254]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 27: Class Coding Basics

*Source: None, pages 946–985*

### Chapter Summary
Chapter 27 content. [^255]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 28: A More Realistic Example

*Source: None, pages 986–1020*

### Chapter Summary
Chapter 28 content. [^256]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 29: Class Coding Details

*Source: None, pages 1021–1060*

### Chapter Summary
Chapter 29 content. [^257]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 30: Operator Overloading

*Source: None, pages 1061–1100*

### Chapter Summary
Chapter 30 content. [^258]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 31: Designing with Classes

*Source: None, pages 1101–1140*

### Chapter Summary
Chapter 31 content. [^259]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 32: Advanced Class Topics

*Source: None, pages 1141–1180*

### Chapter Summary
Chapter 32 content. [^260]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 33: Exception Basics

*Source: None, pages 1181–1215*

### Chapter Summary
Chapter 33 content. [^261]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 34: Exception Coding Details

*Source: None, pages 1216–1250*

### Chapter Summary
Chapter 34 content. [^262]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 35: Exception Objects

*Source: None, pages 1251–1285*

### Chapter Summary
Chapter 35 content. [^263]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 36: Designing with Exceptions

*Source: None, pages 1286–1320*

### Chapter Summary
Chapter 36 content. [^264]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 37: Unicode and Byte Strings

*Source: None, pages 1321–1365*

### Chapter Summary
Chapter 37 content. [^265]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 38: Managed Attributes

*Source: None, pages 1366–1410*

### Chapter Summary
Chapter 38 content. [^266]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 39: Decorators

*Source: None, pages 1411–1455*

### Chapter Summary
Chapter 39 content. [^267]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 40: Metaclasses

*Source: None, pages 1456–1500*

### Chapter Summary
Chapter 40 content. [^268]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 41: All Good Things

*Source: None, pages 1501–1702*

### Chapter Summary
Chapter 41 content. [^269]

### Concept-by-Concept Breakdown


### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---


---

### **Footnotes**

[^1]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 16, lines 1–25).
[^2]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 31, lines 1–8).
[^3]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 20, lines 11–18).
[^4]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 36, lines 1–8).
[^5]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 36, lines 12–19).
[^6]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 21, lines 5–12).
[^7]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 20, lines 13–20).
[^8]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 22, lines 4–11).
[^9]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 24, lines 19–26).
[^10]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 36, lines 10–17).
[^11]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 18, lines 14–20).
[^12]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 34, lines 6–13).
[^13]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 28, lines 2–9).
[^14]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 25, lines 8–15).
[^15]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 25, lines 18–25).
[^16]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 36, lines 11–18).
[^17]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 45, lines 1–1).
[^18]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 77, lines 1–1).
[^19]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 109, lines 1–1).
[^20]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 45, lines 1–25).
[^21]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 76, lines 18–23).
[^22]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 69, lines 5–12).
[^23]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 66, lines 2–9).
[^24]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 56, lines 7–14).
[^25]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 74, lines 4–11).
[^26]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 56, lines 25–31).
[^27]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 66, lines 1–8).
[^28]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 63, lines 12–19).
[^29]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 66, lines 8–15).
[^30]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 56, lines 1–8).
[^31]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 70, lines 2–9).
[^32]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 62, lines 27–28).
[^33]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 64, lines 25–26).
[^34]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 45, lines 5–9).
[^35]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 56, lines 20–27).
[^36]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 77, lines 1–1).
[^37]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 109, lines 1–1).
[^38]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 141, lines 1–1).
[^39]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 77, lines 1–25).
[^40]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 91, lines 2–9).
[^41]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 92, lines 10–17).
[^42]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 93, lines 8–15).
[^43]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 103, lines 2–9).
[^44]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 85, lines 20–27).
[^45]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 107, lines 2–9).
[^46]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 92, lines 10–17).
[^47]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 90, lines 14–19).
[^48]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 92, lines 25–30).
[^49]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 104, lines 1–8).
[^50]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 83, lines 5–12).
[^51]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 79, lines 1–8).
[^52]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 93, lines 8–15).
[^53]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 89, lines 1–8).
[^54]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 107, lines 15–22).
[^55]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 109, lines 1–1).
[^56]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 141, lines 1–1).
[^57]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 176, lines 1–1).
[^58]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 109, lines 1–25).
[^59]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 126, lines 13–20).
[^60]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 134, lines 2–9).
[^61]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 133, lines 13–20).
[^62]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 129, lines 12–19).
[^63]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 136, lines 7–14).
[^64]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 118, lines 19–24).
[^65]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 114, lines 1–8).
[^66]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 130, lines 15–22).
[^67]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 119, lines 10–17).
[^68]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 119, lines 3–10).
[^69]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 118, lines 10–17).
[^70]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 139, lines 3–10).
[^71]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 116, lines 5–12).
[^72]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 110, lines 13–20).
[^73]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 116, lines 8–15).
[^74]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 141, lines 1–1).
[^75]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 176, lines 1–1).
[^76]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 211, lines 1–1).
[^77]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 141, lines 1–25).
[^78]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 160, lines 1–8).
[^79]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 172, lines 6–13).
[^80]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 171, lines 1–8).
[^81]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 141, lines 1–8).
[^82]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 164, lines 5–12).
[^83]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 172, lines 10–17).
[^84]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 142, lines 2–9).
[^85]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 152, lines 4–11).
[^86]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 153, lines 6–13).
[^87]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 152, lines 31–33).
[^88]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 141, lines 24–31).
[^89]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 172, lines 12–19).
[^90]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 170, lines 23–30).
[^91]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 152, lines 29–33).
[^92]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 160, lines 24–27).
[^93]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 176, lines 1–1).
[^94]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 211, lines 1–1).
[^95]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 266, lines 1–1).
[^96]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 176, lines 1–25).
[^97]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 199, lines 6–13).
[^98]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 177, lines 1–8).
[^99]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 177, lines 2–9).
[^100]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 196, lines 3–10).
[^101]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 183, lines 8–15).
[^102]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 180, lines 5–12).
[^103]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 191, lines 3–10).
[^104]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 208, lines 28–32).
[^105]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 197, lines 5–12).
[^106]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 189, lines 16–23).
[^107]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 176, lines 1–8).
[^108]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 180, lines 9–16).
[^109]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 191, lines 9–16).
[^110]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 205, lines 23–30).
[^111]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 180, lines 11–18).
[^112]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 211, lines 1–1).
[^113]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 266, lines 1–1).
[^114]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 316, lines 1–1).
[^115]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 211, lines 1–25).
[^116]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 259, lines 26–31).
[^117]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 239, lines 13–20).
[^118]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 230, lines 10–17).
[^119]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 234, lines 25–29).
[^120]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 234, lines 5–12).
[^121]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 265, lines 7–14).
[^122]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 219, lines 20–21).
[^123]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 232, lines 8–15).
[^124]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 214, lines 7–13).
[^125]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 231, lines 8–15).
[^126]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 218, lines 14–21).
[^127]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 239, lines 1–8).
[^128]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 228, lines 9–16).
[^129]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 233, lines 1–8).
[^130]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 233, lines 1–8).
[^131]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 266, lines 1–1).
[^132]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 316, lines 1–1).
[^133]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 361, lines 1–1).
[^134]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 266, lines 1–25).
[^135]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 267, lines 28–35).
[^136]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 270, lines 7–14).
[^137]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 290, lines 18–25).
[^138]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 298, lines 1–8).
[^139]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 271, lines 5–12).
[^140]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 299, lines 1–8).
[^141]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 290, lines 22–29).
[^142]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 278, lines 14–21).
[^143]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 298, lines 6–13).
[^144]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 280, lines 17–24).
[^145]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 267, lines 1–8).
[^146]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 279, lines 18–25).
[^147]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 279, lines 21–26).
[^148]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 278, lines 6–13).
[^149]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 280, lines 15–22).
[^150]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 316, lines 1–1).
[^151]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 361, lines 1–1).
[^152]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 396, lines 1–1).
[^153]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 316, lines 1–25).
[^154]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 355, lines 12–19).
[^155]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 340, lines 4–11).
[^156]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 354, lines 11–18).
[^157]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 319, lines 5–12).
[^158]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 355, lines 12–19).
[^159]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 349, lines 5–12).
[^160]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 347, lines 1–8).
[^161]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 317, lines 11–18).
[^162]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 332, lines 1–8).
[^163]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 324, lines 6–13).
[^164]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 330, lines 5–12).
[^165]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 347, lines 1–8).
[^166]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 322, lines 16–21).
[^167]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 345, lines 2–9).
[^168]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 321, lines 9–16).
[^169]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 361, lines 1–1).
[^170]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 396, lines 1–1).
[^171]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 436, lines 1–1).
[^172]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 361, lines 1–25).
[^173]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 361, lines 9–16).
[^174]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 394, lines 39–46).
[^175]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 361, lines 9–16).
[^176]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 366, lines 12–19).
[^177]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 383, lines 1–8).
[^178]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 361, lines 23–29).
[^179]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 378, lines 1–8).
[^180]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 394, lines 10–17).
[^181]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 367, lines 5–12).
[^182]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 361, lines 1–8).
[^183]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 373, lines 7–14).
[^184]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 394, lines 7–14).
[^185]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 383, lines 28–35).
[^186]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 371, lines 7–14).
[^187]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 370, lines 2–9).
[^188]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 396, lines 1–1).
[^189]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 436, lines 1–1).
[^190]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 466, lines 1–1).
[^191]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 396, lines 1–25).
[^192]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 417, lines 12–19).
[^193]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 421, lines 15–22).
[^194]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 417, lines 23–30).
[^195]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 421, lines 19–26).
[^196]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 415, lines 8–15).
[^197]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 410, lines 1–8).
[^198]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 410, lines 1–8).
[^199]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 411, lines 11–18).
[^200]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 421, lines 19–26).
[^201]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 417, lines 1–8).
[^202]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 417, lines 1–8).
[^203]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 434, lines 15–22).
[^204]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 400, lines 26–29).
[^205]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 430, lines 12–19).
[^206]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 427, lines 14–19).
[^207]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 436, lines 1–1).
[^208]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 466, lines 1–1).
[^209]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 436, lines 1–25).
[^210]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 436, lines 17–24).
[^211]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 460, lines 12–19).
[^212]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 460, lines 20–24).
[^213]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 460, lines 12–19).
[^214]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 436, lines 5–12).
[^215]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 442, lines 1–8).
[^216]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 436, lines 4–11).
[^217]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 452, lines 1–8).
[^218]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 436, lines 4–11).
[^219]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 448, lines 2–9).
[^220]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 448, lines 10–17).
[^221]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 452, lines 4–11).
[^222]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 437, lines 17–24).
[^223]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 453, lines 6–13).
[^224]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 436, lines 5–12).
[^225]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 466, lines 1–1).
[^226]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 466, lines 1–25).
[^227]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 470, lines 10–17).
[^228]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 470, lines 11–18).
[^229]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 470, lines 10–17).
[^230]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 468, lines 6–13).
[^231]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 478, lines 20–24).
[^232]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 483, lines 4–11).
[^233]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 473, lines 2–9).
[^234]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 493, lines 10–17).
[^235]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 475, lines 19–24).
[^236]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 491, lines 2–9).
[^237]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 496, lines 12–19).
[^238]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 479, lines 23–25).
[^239]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 471, lines 6–13).
[^240]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 468, lines 6–13).
[^241]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 478, lines 4–11).
[^242]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 501, lines 1–25).
[^243]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 541, lines 1–25).
[^244]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 566, lines 1–25).
[^245]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 601, lines 1–25).
[^246]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 636, lines 1–25).
[^247]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 681, lines 1–25).
[^248]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 721, lines 1–25).
[^249]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 756, lines 1–25).
[^250]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 786, lines 1–25).
[^251]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 821, lines 1–25).
[^252]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 851, lines 1–25).
[^253]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 886, lines 1–25).
[^254]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 921, lines 1–25).
[^255]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 946, lines 1–25).
[^256]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 986, lines 1–25).
[^257]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 1021, lines 1–25).
[^258]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 1061, lines 1–25).
[^259]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 1101, lines 1–25).
[^260]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 1141, lines 1–25).
[^261]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 1181, lines 1–25).
[^262]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 1216, lines 1–25).
[^263]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 1251, lines 1–25).
[^264]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 1286, lines 1–25).
[^265]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 1321, lines 1–25).
[^266]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 1366, lines 1–25).
[^267]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 1411, lines 1–25).
[^268]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 1456, lines 1–25).
[^269]: Unknown. *None*. (JSON `Architecture Patterns with Python.json`, p. 1501, lines 1–25).
