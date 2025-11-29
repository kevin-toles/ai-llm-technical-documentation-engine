# Comprehensive Python Guidelines — Building Microservices, 2nd Edition (Chapters 1-15)

*Source: Building Microservices, 2nd Edition, Chapters 1-15*

---

## Chapter 1: What Are Microservices?

*Source: Building Microservices, 2nd Edition, pages 1–28*

### Chapter Summary
Introduces microservices architecture fundamentals, defining what microservices are and their key characteristics including independent deployability, modularity, and service autonomy. Discusses benefits and challenges of distributed systems and compares microservices to monolithic architectures. [^1]

### Concept-by-Concept Breakdown
#### **Gil** *(p.23)*

**Verbatim Educational Excerpt** *(Building Microservices, p.23, lines 7–14)*:
```
Figure 1-2. You can target scaling at just those microservices that need it
Gilt, an online fashion retailer, adopted microservices for this exact reason. Starting in
2007 with a monolithic Rails application, by 2009 Gilt’s system was unable to cope with
the load being placed on it. By splitting out core parts of its system, Gilt was better able to
deal with its traffic spikes, and today has over 450 microservices, each one running on
multiple separate machines.
When embracing on-demand provisioning systems like those provided by Amazon Web
Services, we can even apply this scaling on demand for those pieces that need it. This
```
[^2]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.8)*

**Verbatim Educational Excerpt** *(Building Microservices, p.8, lines 6–11)*:
```
that implementation details always change faster than the thoughts behind them.
Nonetheless, I fully expect that in a few years from now we’ll have learned even more
about where microservices fit, and how to use them well.
So while I have done my best to distill out the essence of the topic in this book, if this
topic interests you, be prepared for many years of continuous learning to keep on top of
the state of the art!
```
[^3]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.17)*

**Verbatim Educational Excerpt** *(Building Microservices, p.17, lines 7–14)*:
```
Within a monolithic system, we fight against these forces by trying to ensure our code is
more cohesive, often by creating abstractions or modules. Cohesion — the drive to have
related code grouped together — is an important concept when we think about
microservices. This is reinforced by Robert C. Martin’s definition of the Single
Responsibility Principle, which states “Gather together those things that change for the
same reason, and separate those things that change for different reasons.”
Microservices take this same approach to independent services. We focus our service
boundaries on business boundaries, making it obvious where code lives for a given piece
```
[^4]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.17)*

**Verbatim Educational Excerpt** *(Building Microservices, p.17, lines 1–8)*:
```
Small, and Focused on Doing One Thing Well
Codebases grow as we write code to add new features. Over time, it can be difficult to
know where a change needs to be made because the codebase is so large. Despite a drive
for clear, modular monolithic codebases, all too often these arbitrary in-process
boundaries break down. Code related to similar functions starts to become spread all over,
making fixing bugs or implementations more difficult.
Within a monolithic system, we fight against these forces by trying to ensure our code is
more cohesive, often by creating abstractions or modules. Cohesion — the drive to have
```
[^5]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 16 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.17)*

**Verbatim Educational Excerpt** *(Building Microservices, p.17, lines 4–11)*:
```
for clear, modular monolithic codebases, all too often these arbitrary in-process
boundaries break down. Code related to similar functions starts to become spread all over,
making fixing bugs or implementations more difficult.
Within a monolithic system, we fight against these forces by trying to ensure our code is
more cohesive, often by creating abstractions or modules. Cohesion — the drive to have
related code grouped together — is an important concept when we think about
microservices. This is reinforced by Robert C. Martin’s definition of the Single
Responsibility Principle, which states “Gather together those things that change for the
```
[^6]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.23)*

**Verbatim Educational Excerpt** *(Building Microservices, p.23, lines 15–16)*:
```
allows us to control our costs more effectively. It’s not often that an architectural approach
can be so closely correlated to an almost immediate cost savings.
```
[^7]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.9)*

**Verbatim Educational Excerpt** *(Building Microservices, p.9, lines 19–26)*:
```
Chapter 3, How to Model Services
Here we’ll start to define the boundary of microservices, using techniques from
domain-driven design to help focus our thinking.
Chapter 4, Integration
This is where we start getting a bit deeper into specific technology implications, as
we discuss what sorts of service collaboration techniques will help us most. We’ll
also delve into the topic of user interfaces and integrating with legacy and
commercial off-the-shelf (COTS) products.
```
[^8]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.7)*

**Verbatim Educational Excerpt** *(Building Microservices, p.7, lines 9–14)*:
```
autonomy of teams, or to more easily embrace new technologies. My own experiences, as
well as those of my colleagues at ThoughtWorks and elsewhere, reinforced the fact that
using larger numbers of services with their own independent lifecycles resulted in more
headaches that had to be dealt with. In many ways, this book was imagined as a one-stop
shop that would help encompass the wide variety of topics that are necessary for
understanding microservices — something that would have helped me greatly in the past!
```
[^9]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.11)*

**Verbatim Educational Excerpt** *(Building Microservices, p.11, lines 3–10)*:
```
Italic
Indicates new terms, URLs, email addresses, filenames, and file extensions.
Constant width
Used for program listings, as well as within paragraphs to refer to program elements
such as variable or function names, databases, data types, environment variables,
statements, and keywords.
Constant width bold
Shows commands or other text that should be typed literally by the user.
```
[^10]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.14)*

**Verbatim Educational Excerpt** *(Building Microservices, p.14, lines 17–21)*:
```
at ThoughtWorks and across the industry who have helped me get this far.
Finally, I would like to thank all the people at O’Reilly, including Mike Loukides for
getting me on board, my editor Brian MacDonald, Rachel Monaghan, Kristen Brown,
Betsy Waliszewski, and all the other people who have helped in ways I may never know
about.
```
[^11]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.15)*

**Verbatim Educational Excerpt** *(Building Microservices, p.15, lines 2–9)*:
```
For many years now, we have been finding better ways to build systems. We have been
learning from what has come before, adopting new technologies, and observing how a
new wave of technology companies operate in different ways to create IT systems that
help make both their customers and their own developers happier.
Eric Evans’s book Domain-Driven Design (Addison-Wesley) helped us understand the
importance of representing the real world in our code, and showed us better ways to model
our systems. The concept of continuous delivery showed how we can more effectively and
efficiently get our software into production, instilling in us the idea that we should treat
```
[^12]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.17)*

**Verbatim Educational Excerpt** *(Building Microservices, p.17, lines 4–11)*:
```
for clear, modular monolithic codebases, all too often these arbitrary in-process
boundaries break down. Code related to similar functions starts to become spread all over,
making fixing bugs or implementations more difficult.
Within a monolithic system, we fight against these forces by trying to ensure our code is
more cohesive, often by creating abstractions or modules. Cohesion — the drive to have
related code grouped together — is an important concept when we think about
microservices. This is reinforced by Robert C. Martin’s definition of the Single
Responsibility Principle, which states “Gather together those things that change for the
```
[^13]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.10)*

**Verbatim Educational Excerpt** *(Building Microservices, p.10, lines 11–18)*:
```
user-to-service and service-to-service authentication and authorization. Security is a
very important topic in computing, one that is all too readily ignored. Although I am
in no way a security expert, I hope that this chapter will at least help you consider
some of the aspects you need to be aware of when building systems, and
microservice systems in particular.
Chapter 10, Conway’s Law and System Design
This chapter focuses on the interplay of organizational structure and architecture.
Many organizations have realized that trouble will occur if you don’t keep the two in
```
[^14]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **List** *(p.10)*

**Verbatim Educational Excerpt** *(Building Microservices, p.10, lines 26–28)*:
```
The final chapter attempts to distill down the core essence of what makes
microservices different. It includes a list of seven microservices principles, as well as
a wrap-up of the key points of the book.
```
[^15]
**Annotation:** This excerpt demonstrates 'list' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Method** *(p.28)*

**Verbatim Educational Excerpt** *(Building Microservices, p.28, lines 4–11)*:
```
completely separate operating system process. Communication between these services
occurs via calls across a network rather than method calls within a process boundary.
SOA emerged as an approach to combat the challenges of the large monolithic
applications. It is an approach that aims to promote the reusability of software; two or
more end-user applications, for example, could both use the same services. It aims to
make it easier to maintain or rewrite software, as theoretically we can replace one service
with another without anyone knowing, as long as the semantics of the service don’t
change too much.
```
[^16]
**Annotation:** This excerpt demonstrates 'method' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 2: How to Model Microservices** *(pp.29–68)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^17]

**Annotation:** Forward reference: Chapter 2 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 3: Splitting the Monolith** *(pp.69–112)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^18]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Microservice Communication Styles** *(pp.113–160)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^19]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 2: How to Model Microservices

*Source: Building Microservices, 2nd Edition, pages 29–68*

### Chapter Summary
Explores how to model microservices using domain-driven design principles. Covers bounded contexts, service boundaries, information hiding, cohesion and coupling, and strategies for decomposing systems into appropriate service boundaries aligned with business capabilities. [^20]

### Concept-by-Concept Breakdown
#### **Gil** *(p.51)*

**Verbatim Educational Excerpt** *(Building Microservices, p.51, lines 4–11)*:
```
The more services we have that do not properly handle the potential failure of downstream
calls, the more fragile our systems will be. This means you will probably want to mandate
as a minimum that each downstream service gets its own connection pool, and you may
even go as far as to say that each also uses a circuit breaker. This will get covered in more
depth when we discuss microservices at scale in Chapter 11.
Playing by the rules is important when it comes to response codes, too. If your circuit
breakers rely on HTTP codes, and one service decides to send back 2XX codes for errors,
or confuses 4XX codes with 5XX codes, then these safety measures can fall apart. Similar
```
[^21]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.48)*

**Verbatim Educational Excerpt** *(Building Microservices, p.48, lines 8–15)*:
```
people, what a good citizen is in one context does not reflect what it looks like somewhere
else. Nonetheless, there are some common characteristics of well-behaved services that I
think are fairly important to observe. These are the few key areas where allowing too
much divergence can result in a pretty torrid time. As Ben Christensen from Netflix puts
it, when we think about the bigger picture, “it needs to be a cohesive system made of
many small parts with autonomous lifecycles but all coming together.” So we need to find
the balance between optimizing for autonomy of the individual microservice without
losing sight of the bigger picture. Defining clear attributes that each service should have is
```
[^22]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.67)*

**Verbatim Educational Excerpt** *(Building Microservices, p.67, lines 3–10)*:
```
systems that model real-world domains. The book is full of great ideas like using
ubiquitous language, repository abstractions, and the like, but there is one very important
concept Evans introduces that completely passed me by at first: bounded context. The idea
is that any given domain consists of multiple bounded contexts, and residing within each
are things (Eric uses the word model a lot, which is probably better than things) that do not
need to be communicated outside as well as things that are shared externally with other
bounded contexts. Each bounded context has an explicit interface, where it decides what
models to share with other contexts.
```
[^23]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.38)*

**Verbatim Educational Excerpt** *(Building Microservices, p.38, lines 2–9)*:
```
Our requirements shift more rapidly than they do for people who design and build
buildings — as do the tools and techniques at our disposal. The things we create are not
fixed points in time. Once launched into production, our software will continue to evolve
as the way it is used changes. For most things we create, we have to accept that once the
software gets into the hands of our customers we will have to react and adapt, rather than
it being a never-changing artifact. Thus, our architects need to shift their thinking away
from creating the perfect end product, and instead focus on helping create a framework in
which the right systems can emerge, and continue to grow as we learn more.
```
[^24]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 14 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.42)*

**Verbatim Educational Excerpt** *(Building Microservices, p.42, lines 2–9)*:
```
Rules are for the obedience of fools and the guidance of wise men.
Generally attributed to Douglas Bader
Making decisions in system design is all about trade-offs, and microservice architectures
give us lots of trade-offs to make! When picking a datastore, do we pick a platform that
we have less experience with, but that gives us better scaling? Is it OK for us to have two
different technology stacks in our system? What about three? Some decisions can be made
completely on the spot with information available to us, and these are the easiest to make.
But what about those decisions that might have to be made on incomplete information?
```
[^25]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.51)*

**Verbatim Educational Excerpt** *(Building Microservices, p.51, lines 6–13)*:
```
as a minimum that each downstream service gets its own connection pool, and you may
even go as far as to say that each also uses a circuit breaker. This will get covered in more
depth when we discuss microservices at scale in Chapter 11.
Playing by the rules is important when it comes to response codes, too. If your circuit
breakers rely on HTTP codes, and one service decides to send back 2XX codes for errors,
or confuses 4XX codes with 5XX codes, then these safety measures can fall apart. Similar
concerns would apply even if you’re not using HTTP; knowing the difference between a
request that was OK and processed correctly, a request that was bad and thus prevented
```
[^26]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.65)*

**Verbatim Educational Excerpt** *(Building Microservices, p.65, lines 5–12)*:
```
important.
What sort of things cause tight coupling? A classic mistake is to pick an integration style
that tightly binds one service to another, causing changes inside the service to require a
change to consumers. We’ll discuss how to avoid this in more depth in Chapter 4.
A loosely coupled service knows as little as it needs to about the services with which it
collaborates. This also means we probably want to limit the number of different types of
calls from one service to another, because beyond the potential performance problem,
chatty communication can lead to tight coupling.
```
[^27]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.38)*

**Verbatim Educational Excerpt** *(Building Microservices, p.38, lines 3–10)*:
```
buildings — as do the tools and techniques at our disposal. The things we create are not
fixed points in time. Once launched into production, our software will continue to evolve
as the way it is used changes. For most things we create, we have to accept that once the
software gets into the hands of our customers we will have to react and adapt, rather than
it being a never-changing artifact. Thus, our architects need to shift their thinking away
from creating the perfect end product, and instead focus on helping create a framework in
which the right systems can emerge, and continue to grow as we learn more.
Although I have spent much of the chapter so far warning you off comparing ourselves too
```
[^28]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.43)*

**Verbatim Educational Excerpt** *(Building Microservices, p.43, lines 2–9)*:
```
The role of the architect is already daunting enough, so luckily we usually don’t have to
also define strategic goals! Strategic goals should speak to where your company is going,
and how it sees itself as best making its customers happy. These will be high-level goals,
and may not include technology at all. They could be defined at a company level or a
division level. They might be things like “Expand into Southeast Asia to unlock new
markets,” or “Let the customer achieve as much as possible using self-service.” The key is
that this is where your organization is headed, so you need to make sure the technology is
aligned to it.
```
[^29]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.48)*

**Verbatim Educational Excerpt** *(Building Microservices, p.48, lines 8–15)*:
```
people, what a good citizen is in one context does not reflect what it looks like somewhere
else. Nonetheless, there are some common characteristics of well-behaved services that I
think are fairly important to observe. These are the few key areas where allowing too
much divergence can result in a pretty torrid time. As Ben Christensen from Netflix puts
it, when we think about the bigger picture, “it needs to be a cohesive system made of
many small parts with autonomous lifecycles but all coming together.” So we need to find
the balance between optimizing for autonomy of the individual microservice without
losing sight of the bigger picture. Defining clear attributes that each service should have is
```
[^30]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.57)*

**Verbatim Educational Excerpt** *(Building Microservices, p.57, lines 1–8)*:
```
Exception Handling
So our principles and practices guide how our systems should be built. But what happens
when our system deviates from this? Sometimes we make a decision that is just an
exception to the rule. In these cases, it might be worth capturing such a decision in a log
somewhere for future reference. If enough exceptions are found, it may eventually make
sense to change the principle or practice to reflect a new understanding of the world. For
example, we might have a practice that states that we will always use MySQL for data
storage. But then we see compelling reasons to use Cassandra for highly scalable storage,
```
[^31]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.57)*

**Verbatim Educational Excerpt** *(Building Microservices, p.57, lines 1–8)*:
```
Exception Handling
So our principles and practices guide how our systems should be built. But what happens
when our system deviates from this? Sometimes we make a decision that is just an
exception to the rule. In these cases, it might be worth capturing such a decision in a log
somewhere for future reference. If enough exceptions are found, it may eventually make
sense to change the principle or practice to reflect a new understanding of the world. For
example, we might have a practice that states that we will always use MySQL for data
storage. But then we see compelling reasons to use Cassandra for highly scalable storage,
```
[^32]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.36)*

**Verbatim Educational Excerpt** *(Building Microservices, p.36, lines 2–9)*:
```
You keep using that word. I do not think it means what you think it means.
Inigo Montoya, from The Princess Bride
Architects have an important job. They are in charge of making sure we have a joined-up
technical vision, one that should help us deliver the system our customers need. In some
places, they may only have to work with one team, in which case the role of the architect
and technical lead is often the same. In others, they may be defining the vision for an
entire program of work, coordinating with multiple teams across the world, or perhaps
even an entire organization. At whatever level they operate, the role is a tricky one to pin
```
[^33]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.67)*

**Verbatim Educational Excerpt** *(Building Microservices, p.67, lines 12–19)*:
```
explicit boundaries.”1 If you want information from a bounded context, or want to make
requests of functionality within a bounded context, you communicate with its explicit
boundary using models. In his book, Evans uses the analogy of cells, where “[c]ells can
exist because their membranes define what is in and out and determine what can pass.”
Let’s return for a moment to the MusicCorp business. Our domain is the whole business in
which we are operating. It covers everything from the warehouse to the reception desk,
from finance to ordering. We may or may not model all of that in our software, but that is
nonetheless the domain in which we are operating. Let’s think about parts of that domain
```
[^34]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.36)*

**Verbatim Educational Excerpt** *(Building Microservices, p.36, lines 3–10)*:
```
Inigo Montoya, from The Princess Bride
Architects have an important job. They are in charge of making sure we have a joined-up
technical vision, one that should help us deliver the system our customers need. In some
places, they may only have to work with one team, in which case the role of the architect
and technical lead is often the same. In others, they may be defining the vision for an
entire program of work, coordinating with multiple teams across the world, or perhaps
even an entire organization. At whatever level they operate, the role is a tricky one to pin
down, and despite it often being the obvious career progression for developers in
```
[^35]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 3: Splitting the Monolith** *(pp.69–112)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^36]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Microservice Communication Styles** *(pp.113–160)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^37]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Implementing Microservice Communication** *(pp.161–208)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^38]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 3: Splitting the Monolith

*Source: Building Microservices, 2nd Edition, pages 69–112*

### Chapter Summary
Details strategies for migrating from monolithic applications to microservices architecture. Covers the strangler pattern, incremental decomposition, database splitting techniques, parallel running, and practical approaches to modernizing legacy systems while maintaining business continuity. [^39]

### Concept-by-Concept Breakdown
#### **None** *(p.71)*

**Verbatim Educational Excerpt** *(Building Microservices, p.71, lines 8–15)*:
```
Although there was some code reuse very early on between the SnapCI and Go-CD
projects, in the end SnapCI turned out to be a completely new codebase. Nonetheless, the
previous experience of the team in the domain of CD tooling emboldened them to move
more quickly in identifying boundaries, and building their system as a set of
microservices.
After a few months, though, it became clear that the use cases of SnapCI were subtly
different enough that the initial take on the service boundaries wasn’t quite right. This led
to lots of changes being made across services, and an associated high cost of change.
```
[^40]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.95)*

**Verbatim Educational Excerpt** *(Building Microservices, p.95, lines 10–17)*:
```
more thought is likely to get you in trouble. In some of the worst examples, developers
may be using remote calls without knowing it if the abstraction is overly opaque.
You need to think about the network itself. Famously, the first of the fallacies of
distributed computing is “The network is reliable”. Networks aren’t reliable. They can and
will fail, even if your client and the server you are speaking to are fine. They can fail fast,
they can fail slow, and they can even malform your packets. You should assume that your
networks are plagued with malevolent entities ready to unleash their ire on a whim.
Therefore, the failure modes you can expect are different. A failure could be caused by the
```
[^41]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.81)*

**Verbatim Educational Excerpt** *(Building Microservices, p.81, lines 1–5)*:
```
Looking for the Ideal Integration Technology
There is a bewildering array of options out there for how one microservice can talk to
another. But which is the right one: SOAP? XML-RPC? REST? Protocol buffers? We’ll
dive into those in a moment, but before we do, let’s think about what we want out of
whatever technology we pick.
```
[^42]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.110)*

**Verbatim Educational Excerpt** *(Building Microservices, p.110, lines 1–8)*:
```
Complexities of Asynchronous Architectures
Some of this asynchronous stuff seems fun, right? Event-driven architectures seem to lead
to significantly more decoupled, scalable systems. And they can. But these programming
styles do lead to an increase in complexity. This isn’t just the complexity required to
manage publishing and subscribing to messages as we just discussed, but also in the other
problems we might face. For example, when considering long-running async
request/response, we have to think about what to do when the response comes back. Does
it come back to the same node that initiated the request? If so, what if that node is down?
```
[^43]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 25 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.89)*

**Verbatim Educational Excerpt** *(Building Microservices, p.89, lines 1–8)*:
```
Synchronous Versus Asynchronous
Before we start diving into the specifics of different technology choices, we should discuss
one of the most important decisions we can make in terms of how services collaborate.
Should communication be synchronous or asynchronous? This fundamental choice
inevitably guides us toward certain implementation detail.
With synchronous communication, a call is made to a remote server, which blocks until
the operation completes. With asynchronous communication, the caller doesn’t wait for
the operation to complete before returning, and may not even care whether or not the
```
[^44]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.80)*

**Verbatim Educational Excerpt** *(Building Microservices, p.80, lines 4–7)*:
```
autonomy, allowing you to change and release them independent of the whole. Get it
wrong, and disaster awaits. Hopefully once you’ve read this chapter you’ll learn how to
avoid some of the biggest pitfalls that have plagued other attempts at SOA and could yet
await you in your journey to microservices.
```
[^45]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.87)*

**Verbatim Educational Excerpt** *(Building Microservices, p.87, lines 15–22)*:
```
with all other parties with access to the database. If I decide to change my schema to better
represent my data, or make my system easier to maintain, I can break my consumers. The
DB is effectively a very large, shared API that is also quite brittle. If I want to change the
logic associated with, say, how the helpdesk manages customers and this requires a change
to the database, I have to be extremely careful that I don’t break parts of the schema used
by other services. This situation normally results in requiring a large amount of regression
testing.
Second, my consumers are tied to a specific technology choice. Perhaps right now it
```
[^46]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.96)*

**Verbatim Educational Excerpt** *(Building Microservices, p.96, lines 29–36)*:
```
looks like:
public class Customer implements Serializable {
  private String firstName;
  private String surname;
  private String emailAddress;
  private String age;
}
Now, what if it turns out that although we expose the age field in our Customer objects,
```
[^47]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.93)*

**Verbatim Educational Excerpt** *(Building Microservices, p.93, lines 3–10)*:
```
on a remote service somewhere. There are a number of different types of RPC technology
out there. Some of this technology relies on having an interface definition (SOAP, Thrift,
protocol buffers). The use of a separate interface definition can make it easier to generate
client and server stubs for different technology stacks, so, for example, I could have a Java
server exposing a SOAP interface, and a .NET client generated from the Web Service
Definition Language (WSDL) definition of the interface. Other technology, like Java RMI,
calls for a tighter coupling between the client and server, requiring that both use the same
underlying technology but avoid the need for a shared interface definition. All these
```
[^48]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Dictionary** *(p.97)*

**Verbatim Educational Excerpt** *(Building Microservices, p.97, lines 6–12)*:
```
naming type to make it easier to manage. I could, of course, fix this by passing around
dictionary types as the parameters of my calls, but at that point, I lose many of the benefits
of the generated stubs because I’ll still have to manually match and extract the fields I
want.
In practice, objects used as part of binary serialization across the wire can be thought of as
expand-only types. This brittleness results in the types being exposed over the wire and
becoming a mass of fields, some of which are no longer used but can’t be safely removed.
```
[^49]
**Annotation:** This excerpt demonstrates 'dictionary' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.89)*

**Verbatim Educational Excerpt** *(Building Microservices, p.89, lines 26–33)*:
```
asking for things to be done, it instead says this thing happened and expects other parties
to know what to do. We never tell anyone else what to do. Event-based systems by their
nature are asynchronous. The smarts are more evenly distributed — that is, the business
logic is not centralized into core brains, but instead pushed out more evenly to the various
collaborators. Event-based collaboration is also highly decoupled. The client that emits an
event doesn’t have any way of knowing who or what will react to it, which also means that
you can add new subscribers to these events without the client ever needing to know.
So are there any other drivers that might push us to pick one style over another? One
```
[^50]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Encoding** *(p.109)*

**Verbatim Educational Excerpt** *(Building Microservices, p.109, lines 7–8)*:
```
considerations apply as with synchronous communication. If you are currently happy with
encoding requests and responses using JSON, stick with it.
```
[^51]
**Annotation:** This excerpt demonstrates 'encoding' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.96)*

**Verbatim Educational Excerpt** *(Building Microservices, p.96, lines 8–15)*:
```
import java.rmi.Remote;
import java.rmi.RemoteException;
public interface CustomerRemote extends Remote {
 public Customer findCustomer(String id) throws RemoteException;
 public Customer createCustomer(String firstname, String surname, String emailAddress)
     throws RemoteException;
}
In this interface, findCustomer takes the first name, surname, and email address. What
```
[^52]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.96)*

**Verbatim Educational Excerpt** *(Building Microservices, p.96, lines 8–15)*:
```
import java.rmi.Remote;
import java.rmi.RemoteException;
public interface CustomerRemote extends Remote {
 public Customer findCustomer(String id) throws RemoteException;
 public Customer createCustomer(String firstname, String surname, String emailAddress)
     throws RemoteException;
}
In this interface, findCustomer takes the first name, surname, and email address. What
```
[^53]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.104)*

**Verbatim Educational Excerpt** *(Building Microservices, p.104, lines 14–21)*:
```
the microservice, until the interface had stabilized enough. For an interim period, entities
were just persisted in a file on local disk, which is obviously not a suitable long-term
solution. This ensured that how the consumers wanted to use the service drove the design
and implementation decisions. The rationale given, which was borne out in the results,
was that it is too easy for the way we store domain entities in a backing store to overtly
influence the models we send over the wire to collaborators. One of the downsides with
this approach is that we are deferring the work required to wire up our data store. I think
for new service boundaries, however, this is an acceptable trade-off.
```
[^54]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 4: Microservice Communication Styles** *(pp.113–160)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^55]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Implementing Microservice Communication** *(pp.161–208)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^56]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Workflow** *(pp.209–242)*

This later chapter builds upon the concepts introduced here, particularly: abstraction, as, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^57]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts abstraction, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 4: Microservice Communication Styles

*Source: Building Microservices, 2nd Edition, pages 113–160*

### Chapter Summary
Examines different communication styles for microservices including synchronous (REST, RPC) and asynchronous (messaging, events) approaches. Discusses choreography vs orchestration, event-driven architecture, and choosing appropriate communication patterns for different scenarios. [^58]

### Concept-by-Concept Breakdown
#### **None** *(p.136)*

**Verbatim Educational Excerpt** *(Building Microservices, p.136, lines 8–15)*:
```
might write software for your own internal purposes or for an external client, or both.
Nonetheless, even if you are an organization with the ability to create a significant amount
of custom software, you’ll still use software products provided by external parties, be they
commercial or open source. Why is this?
First, your organization almost certainly has a greater demand for software than can be
satisfied internally. Think of all the products you use, from office productivity tools like
Excel to operating systems to payroll systems. Creating all of those for your own use
would be a mammoth undertaking. Second, and most important, it wouldn’t be cost
```
[^59]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.114)*

**Verbatim Educational Excerpt** *(Building Microservices, p.114, lines 10–17)*:
```
DRY is what leads us to create code that can be reused. We pull duplicated code into
abstractions that we can then call from multiple places. Perhaps we go as far as making a
shared library that we can use everywhere! This approach, however, can be deceptively
dangerous in a microservice architecture.
One of the things we want to avoid at all costs is overly coupling a microservice and
consumers such that any small change to the microservice itself can cause unnecessary
changes to the consumer. Sometimes, however, the use of shared code can create this very
coupling. For example, at one client we had a library of common domain objects that
```
[^60]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.115)*

**Verbatim Educational Excerpt** *(Building Microservices, p.115, lines 2–9)*:
```
I’ve spoken to more than one team who has insisted that creating client libraries for your
services is an essential part of creating services in the first place. The argument is that this
makes it easy to use your service, and avoids the duplication of code required to consume
the service itself.
The problem, of course, is that if the same people create both the server API and the client
API, there is the danger that logic that should exist on the server starts leaking into the
client. I should know: I’ve done this myself. The more logic that creeps into the client
library, the more cohesion starts to break down, and you find yourself having to change
```
[^61]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.160)*

**Verbatim Educational Excerpt** *(Building Microservices, p.160, lines 1–8)*:
```
Example: Shared Static Data
I have seen perhaps as many country codes stored in databases (shown in Figure 5-4) as I
have written StringUtils classes for in-house Java projects. This seems to imply that we
plan to change the countries our system supports way more frequently than we’ll deploy
new code, but whatever the real reason, these examples of shared static data being stored
in databases come up a lot. So what do we do in our music shop if all our potential
services read from the same table like this?
Figure 5-4. Country codes in the database
```
[^62]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 19 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.119)*

**Verbatim Educational Excerpt** *(Building Microservices, p.119, lines 1–8)*:
```
Defer It for as Long as Possible
The best way to reduce the impact of making breaking changes is to avoid making them in
the first place. You can achieve much of this by picking the right integration technology,
as we’ve discussed throughout this chapter. Database integration is a great example of
technology that can make it very hard to avoid breaking changes. REST, on the other
hand, helps because changes to internal implementation detail are less likely to result in a
change to the service interface.
Another key to deferring a breaking change is to encourage good behavior in your clients,
```
[^63]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.160)*

**Verbatim Educational Excerpt** *(Building Microservices, p.160, lines 2–9)*:
```
I have seen perhaps as many country codes stored in databases (shown in Figure 5-4) as I
have written StringUtils classes for in-house Java projects. This seems to imply that we
plan to change the countries our system supports way more frequently than we’ll deploy
new code, but whatever the real reason, these examples of shared static data being stored
in databases come up a lot. So what do we do in our music shop if all our potential
services read from the same table like this?
Figure 5-4. Country codes in the database
Well, we have a few options. One is to duplicate this table for each of our packages, with
```
[^64]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.119)*

**Verbatim Educational Excerpt** *(Building Microservices, p.119, lines 1–8)*:
```
Defer It for as Long as Possible
The best way to reduce the impact of making breaking changes is to avoid making them in
the first place. You can achieve much of this by picking the right integration technology,
as we’ve discussed throughout this chapter. Database integration is a great example of
technology that can make it very hard to avoid breaking changes. REST, on the other
hand, helps because changes to internal implementation detail are less likely to result in a
change to the service interface.
Another key to deferring a breaking change is to encourage good behavior in your clients,
```
[^65]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.116)*

**Verbatim Educational Excerpt** *(Building Microservices, p.116, lines 10–17)*:
```
what that resource looked like when we made the request. It is possible that after we
requested that Customer resource, something else has changed it. What we have in effect
is a memory of what the Customer resource once looked like. The longer we hold on to
this memory, the higher the chance that this memory will be false. Of course, if we avoid
requesting data more than we need to, our systems can become much more efficient.
Sometimes this memory is good enough. Other times you need to know if it has changed.
So whether you decide to pass around a memory of what an entity once looked like, make
sure you also include a reference to the original resource so that the new state can be
```
[^66]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.146)*

**Verbatim Educational Excerpt** *(Building Microservices, p.146, lines 20–21)*:
```
we need. All other mainstream programming languages have similar concepts built in,
with JavaScript very arguably being an exception.
```
[^67]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.146)*

**Verbatim Educational Excerpt** *(Building Microservices, p.146, lines 20–21)*:
```
we need. All other mainstream programming languages have similar concepts built in,
with JavaScript very arguably being an exception.
```
[^68]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.160)*

**Verbatim Educational Excerpt** *(Building Microservices, p.160, lines 13–20)*:
```
A second option is to instead treat this shared, static data as code. Perhaps it could be in a
property file deployed as part of the service, or perhaps just as an enumeration. The
problems around the consistency of data remain, although experience has shown that it is
far easier to push out changes to configuration files than alter live database tables. This is
often a very sensible approach.
A third option, which may well be extreme, is to push this static data into a service of its
own right. In a couple of situations I have encountered, the volume, complexity, and rules
associated with the static reference data were sufficient that this approach was warranted,
```
[^69]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.115)*

**Verbatim Educational Excerpt** *(Building Microservices, p.115, lines 35–38)*:
```
you’ll allow people using different technology stacks to make calls to the underlying API.
And finally, make sure that the clients are in charge of when to upgrade their client
libraries: we need to ensure we maintain the ability to release our services independently
of each other!
```
[^70]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.156)*

**Verbatim Educational Excerpt** *(Building Microservices, p.156, lines 2–9)*:
```
The first step is to take a look at the code itself and see which parts of it read to and write
from the database. A common practice is to have a repository layer, backed by some sort
of framework like Hibernate, to bind your code to the database, making it easy to map
objects or data structures to and from the database. If you have been following along so
far, you’ll have grouped our code into packages representing our bounded contexts; we
want to do the same for our database access code. This may require splitting up the
repository layer into several parts, as shown in Figure 5-1.
Figure 5-1. Splitting out our repository layers
```
[^71]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.122)*

**Verbatim Educational Excerpt** *(Building Microservices, p.122, lines 5–12)*:
```
MAJOR.MINOR.PATCH. When the MAJOR number increments, it means that backward
incompatible changes have been made. When MINOR increments, new functionality has
been added that should be backward compatible. Finally, a change to PATCH states that bug
fixes have been made to existing functionality.
To see how useful semantic versioning can be, let’s look at a simple use case. Our
helpdesk application is built to work against version 1.2.0 of the customer service. If a
new feature is added, causing the customer service to change to 1.3.0, our helpdesk
application should see no change in behavior and shouldn’t be expected to make any
```
[^72]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Global** *(p.129)*

**Verbatim Educational Excerpt** *(Building Microservices, p.129, lines 12–18)*:
```
services via SMS in places where bandwidth is at a premium — the use of SMS as an
interface is huge in the global south, for example.
So, although our core services — our core offering — might be the same, we need a way
to adapt them for the different constraints that exist for each type of interface. When we
look at different styles of user interface composition, we need to ensure that they address
this challenge. Let’s look at a few models of user interfaces to see how this might be
achieved.
```
[^73]
**Annotation:** This excerpt demonstrates 'global' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 5: Implementing Microservice Communication** *(pp.161–208)*

This later chapter builds upon the concepts introduced here, particularly: None, abstraction, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^74]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, abstraction appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Workflow** *(pp.209–242)*

This later chapter builds upon the concepts introduced here, particularly: abstraction, as, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^75]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts abstraction, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Build** *(pp.243–272)*

This later chapter builds upon the concepts introduced here, particularly: as, break, def.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^76]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 5: Implementing Microservice Communication

*Source: Building Microservices, 2nd Edition, pages 161–208*

### Chapter Summary
Provides detailed implementation guidance for microservice communication including REST APIs, RPC frameworks (gRPC), GraphQL, message brokers (Kafka, RabbitMQ), API gateways, and service mesh technologies. Covers protocol selection and serialization formats. [^77]

### Concept-by-Concept Breakdown
#### **None** *(p.167)*

**Verbatim Educational Excerpt** *(Building Microservices, p.167, lines 2–9)*:
```
Transactions are useful things. They allow us to say these events either all happen
together, or none of them happen. They are very useful when we’re inserting data into a
database; they let us update multiple tables at once, knowing that if anything fails,
everything gets rolled back, ensuring our data doesn’t get into an inconsistent state.
Simply put, a transaction allows us to group together multiple different activities that take
our system from one consistent state to another — everything works, or nothing changes.
Transactions don’t just apply to databases, although we most often use them in that
context. Message brokers, for example, have long allowed you to post and receive
```
[^78]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.198)*

**Verbatim Educational Excerpt** *(Building Microservices, p.198, lines 14–21)*:
```
The downside can be the difficulty in creating the packages in the first place. For Linux,
the FPM package manager tool gives a nicer abstraction for creating Linux OS packages,
and converting from a tarball-based deployment to an OS-based deployment can be fairly
straightforward. The Windows space is somewhat trickier. The native packaging system in
the form of MSI installers and the like leave a lot to be desired when compared to the
capabilities in the Linux space. The NuGet package system has started to help address
this, at least in terms of helping manage development libraries. More recently, Chocolatey
NuGet has extended these ideas, providing a package manager for Windows designed for
```
[^79]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.194)*

**Verbatim Educational Excerpt** *(Building Microservices, p.194, lines 2–9)*:
```
Very early on in using continuous integration, we realized the value in sometimes having
multiple stages inside a build. Tests are a very common case where this comes into play. I
may have a lot of fast, small-scoped tests, and a small number of large-scoped, slow tests.
If we run all the tests together, we may not be able to get fast feedback when our fast tests
fail if we’re waiting for our long-scoped slow tests to finally finish. And if the fast tests
fail, there probably isn’t much sense in running the slower tests anyway! A solution to this
problem is to have different stages in our build, creating what is known as a build pipeline.
One stage for the faster tests, one for the slower tests.
```
[^80]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 26 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.166)*

**Verbatim Educational Excerpt** *(Building Microservices, p.166, lines 1–8)*:
```
Staging the Break
So we’ve found seams in our application code, grouping it around bounded contexts.
We’ve used this to identify seams in the database, and we’ve done our best to split those
out. What next? Do you do a big-bang release, going from one monolithic service with a
single schema to two services, each with its own schema? I would actually recommend
that you split out the schema but keep the service together before splitting the application
code out into separate microservices, as shown in Figure 5-9.
Figure 5-9. Staging a service separation
```
[^81]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.185)*

**Verbatim Educational Excerpt** *(Building Microservices, p.185, lines 23–29)*:
```
A great technique here is to adapt an approach more typically taught for the design of
object-oriented systems: class-responsibility-collaboration (CRC) cards. With CRC cards,
you write on one index card the name of the class, what its responsibilities are, and who it
collaborates with. When working through a proposed design, for each service I list its
responsibilities in terms of the capabilities it provides, with the collaborators specified in
the diagram. As you work through more use cases, you start to get a sense as to whether
all of this hangs together properly.
```
[^82]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.204)*

**Verbatim Educational Excerpt** *(Building Microservices, p.204, lines 6–13)*:
```
production. Our microservice should be the same throughout, but the environment will be
different. At the very least, they’ll be separate, distinct collections of configuration and
hosts. But often they can vary much more than that. For example, our production
environment for our service might consist of multiple load-balanced hosts spread across
two data centers, whereas our test environment might just have everything running on a
single host. These differences in environments can introduce a few problems.
I was bitten by this personally many years ago. We were deploying a Java web service into
a clustered WebLogic application container in production. This WebLogic cluster
```
[^83]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.166)*

**Verbatim Educational Excerpt** *(Building Microservices, p.166, lines 14–18)*:
```
discussing this next. By splitting the schemas out but keeping the application code
together, we give ourselves the ability to revert our changes or continue to tweak things
without impacting any consumers of our service. Once we are satisfied that the DB
separation makes sense, we can then think about splitting out the application code into two
services.
```
[^84]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.178)*

**Verbatim Educational Excerpt** *(Building Microservices, p.178, lines 6–11)*:
```
without the overhead of being sent over HTTP; instead, the system could simply save a
CSV file to a shared location.
I have seen the preceding approach used for batch insertion of data, where it worked well.
I am less in favor of it for reporting systems, however, as I feel that there are other,
potentially simpler solutions that can scale more effectively when you’re dealing with
traditional reporting needs.
```
[^85]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.192)*

**Verbatim Educational Excerpt** *(Building Microservices, p.192, lines 7–14)*:
```
multiple CI builds mapping to parts of this source tree, as we see in Figure 6-2. With well-
defined structure, you can easily map the builds to certain parts of the source tree. In
general, I am not a fan of this approach, as this model can be a mixed blessing. On the one
hand, my check-in/check-out process can be simpler as I have only one repository to
worry about. On the other hand, it becomes very easy to get into the habit of checking in
source code for multiple services at once, which can make it equally easy to slip into
making changes that couple services together. I would greatly prefer this approach,
however, over having a single build for multiple services.
```
[^86]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.171)*

**Verbatim Educational Excerpt** *(Building Microservices, p.171, lines 10–17)*:
```
the logic to handle the compensating transaction live in the customer service, the order
service, or somewhere else?
But what happens if our compensating transaction fails? It’s certainly possible. Then we’d
have an order in the order table with no matching pick instruction. In this situation, you’d
either need to retry the compensating transaction, or allow some backend process to clean
up the inconsistency later on. This could be something as simple as a maintenance screen
that admin staff had access to, or an automated process.
Now think about what happens if we have not one or two operations we want to be
```
[^87]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.196)*

**Verbatim Educational Excerpt** *(Building Microservices, p.196, lines 1–8)*:
```
And the Inevitable Exceptions
As with all good rules, there are exceptions we need to consider too. The “one
microservice per build” approach is absolutely something you should aim for, but are there
times when something else makes sense? When a team is starting out with a new project,
especially a greenfield one where they are working with a blank sheet of paper, it is quite
likely that there will be a large amount of churn in terms of working out where the service
boundaries lie. This is a good reason, in fact, for keeping your initial services on the larger
side until your understanding of the domain stabilizes.
```
[^88]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.196)*

**Verbatim Educational Excerpt** *(Building Microservices, p.196, lines 1–8)*:
```
And the Inevitable Exceptions
As with all good rules, there are exceptions we need to consider too. The “one
microservice per build” approach is absolutely something you should aim for, but are there
times when something else makes sense? When a team is starting out with a new project,
especially a greenfield one where they are working with a blank sheet of paper, it is quite
likely that there will be a large amount of churn in terms of working out where the service
boundaries lie. This is a good reason, in fact, for keeping your initial services on the larger
side until your understanding of the domain stabilizes.
```
[^89]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.197)*

**Verbatim Educational Excerpt** *(Building Microservices, p.197, lines 2–9)*:
```
Most technology stacks have some sort of first-class artifact, along with tools to support
creating and installing them. Ruby has gems, Java has JAR files and WAR files, and
Python has eggs. Developers with experience in one of these stacks will be well versed in
working with (and hopefully creating) these artifacts.
From the point of view of a microservice, though, depending on your technology stack,
this artifact may not be enough by itself. While a Java JAR file can be made to be
executable and run an embedded HTTP process, for things like Ruby and Python
applications, you’ll expect to use a process manager running inside Apache or Nginx. So
```
[^90]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.176)*

**Verbatim Educational Excerpt** *(Building Microservices, p.176, lines 7–14)*:
```
purpose.
Finally, the database options available to us have exploded recently. While standard
relational databases expose SQL query interfaces that work with many reporting tools,
they aren’t always the best option for storing data for our running services. What if our
application data is better modeled as a graph, as in Neo4j? Or what if we’d rather use a
document store like MongoDB? Likewise, what if we wanted to explore using a column-
oriented database like Cassandra for our reporting system, which makes it much easier to
scale for larger volumes? Being constrained in having to have one database for both
```
[^91]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.175)*

**Verbatim Educational Excerpt** *(Building Microservices, p.175, lines 1–8)*:
```
The Reporting Database
Reporting typically needs to group together data from across multiple parts of our
organization in order to generate useful output. For example, we might want to enrich the
data from our general ledger with descriptions of what was sold, which we get from a
catalog. Or we might want to look at the shopping behavior of specific, high-value
customers, which could require information from their purchase history and their customer
profile.
In a standard, monolithic service architecture, all our data is stored in one big database.
```
[^92]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 6: Workflow** *(pp.209–242)*

This later chapter builds upon the concepts introduced here, particularly: abstraction, as, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^93]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts abstraction, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Build** *(pp.243–272)*

This later chapter builds upon the concepts introduced here, particularly: as, break, collections.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^94]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Deployment** *(pp.273–312)*

This later chapter builds upon the concepts introduced here, particularly: None, as, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^95]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 6: Workflow

*Source: Building Microservices, 2nd Edition, pages 209–242*

### Chapter Summary
Explores workflow management in distributed systems including orchestration and choreography patterns. Covers saga pattern for distributed transactions, compensation mechanisms, long-running processes, state machines, and coordinating business processes across multiple services. [^96]

### Concept-by-Concept Breakdown
#### **Gil** *(p.216)*

**Verbatim Educational Excerpt** *(Building Microservices, p.216, lines 14–21)*:
```
over 60–70 services.
This sort of pattern is also borne out by the experiences of Gilt, an online fashion retailer
that started in 2007. Gilt’s monolithic Rails application was starting to become difficult to
scale, and the company decided in 2009 to start decomposing the system into
microservices. Again automation, especially tooling to help developers, was given as a
key reason to drive Gilt’s explosion in the use of microservices. A year later, Gilt had
around 10 microservices live; by 2012, over 100; and in 2014, over 450 microservices by
Gilt’s own count — in other words, around three services for every developer in Gilt.
```
[^97]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.224)*

**Verbatim Educational Excerpt** *(Building Microservices, p.224, lines 7–14)*:
```
applications.
The Docker app abstraction is a useful one for us, because just as with VM images the
underlying technology used to implement the service is hidden from us. We have our
builds for our services create Docker applications, and store them in the Docker registry,
and away we go.
Docker can also alleviate some of the downsides of running lots of services locally for dev
and test purposes. Rather than using Vagrant to host multiple independent VMs, each one
containing its own service, we can host a single VM in Vagrant that runs a Docker
```
[^98]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.214)*

**Verbatim Educational Excerpt** *(Building Microservices, p.214, lines 1–8)*:
```
Platform as a Service
When using a platform as a service (PaaS), you are working at a higher-level abstraction
than at a single host. Most of these platforms rely on taking a technology-specific artifact,
such as a Java WAR file or Ruby gem, and automatically provisioning and running it for
you. Some of these platforms will transparently attempt to handle scaling the system up
and down for you, although a more common (and in my experience less error-prone) way
will allow you some control over how many nodes your service might run on, but it
handles the rest.
```
[^99]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 20 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.215)*

**Verbatim Educational Excerpt** *(Building Microservices, p.215, lines 6–13)*:
```
to be constrained by the number of terminal windows I could have open at once — a
second monitor was a huge step up. This breaks down really fast, though.
One of the pushbacks against the single-service-per-host setup is the perception that the
amount of overhead to manage these hosts will increase. This is certainly true if you are
doing everything manually. Double the servers, double the work! But if we automate
control of our hosts, and deployment of the services, then there is no reason why adding
more hosts should increase our workload in a linear fashion.
But even if we keep the number of hosts small, we still are going to have lots of services.
```
[^100]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.214)*

**Verbatim Educational Excerpt** *(Building Microservices, p.214, lines 9–16)*:
```
At the time of writing, most of the best, most polished PaaS solutions are hosted. Heroku
comes to mind as being probably the gold class of PaaS. It doesn’t just handle running
your service, it also supports services like databases in a very simple fashion. Self-hosted
solutions do exist in this space, although they are more immature than the hosted
solutions.
When PaaS solutions work well, they work very well indeed. However, when they don’t
quite work for you, you often don’t have much control in terms of getting under the hood
to fix things. This is part of the trade-off you make. I would say that in my experience the
```
[^101]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.228)*

**Verbatim Educational Excerpt** *(Building Microservices, p.228, lines 1–8)*:
```
Environment Definition
Clearly, for this to work, we need to have some way of defining what our environments
look like, and what our service looks like in a given environment. You can think of an
environment definition as a mapping from a microservice to compute, network, and
storage resources. I’ve done this with YAML files before, and used my scripts to pull this
data in. Example 6-1 is a simplified version of some work I did a couple of years ago for a
project that used AWS.
Example 6-1. An example environment definition
```
[^102]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.209)*

**Verbatim Educational Excerpt** *(Building Microservices, p.209, lines 3–10)*:
```
services it ran, hit this problem. Initially it coexisted many services on a single box, but
uneven load on one of the services would have an adverse impact on everything else
running on that host. This makes impact analysis of host failures more complex as well —
taking a single host out of commission can have a large ripple effect.
Deployment of services can be somewhat more complex too, as ensuring one deployment
doesn’t affect another leads to additional headaches. For example, if I use Puppet to
prepare a host, but each service has different (and potentially contradictory) dependencies,
how can I make that work? In the worst-case scenario, I have seen people tie multiple
```
[^103]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.220)*

**Verbatim Educational Excerpt** *(Building Microservices, p.220, lines 4–11)*:
```
Underneath, it uses a standard virtualization system (typically VirtualBox, although it can
use other platforms). It allows you to define a set of VMs in a text file, along with how the
VMs are networked together and which images the VMs should be based on. This text file
can be checked in and shared between team members.
This makes it easier for you to create production-like environments on your local machine.
You can spin up multiple VMs at a time, shut individual ones to test failure modes, and
have the VMs mapped through to local directories so you can make changes and see them
reflected immediately. Even for teams using on-demand cloud platforms like AWS, the
```
[^104]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.230)*

**Verbatim Educational Excerpt** *(Building Microservices, p.230, lines 16–21)*:
```
developers, testers, and operations people alike.
Finally, if you want to go deeper into this topic, I thoroughly recommend you read Jez
Humble and David Farley’s Continuous Delivery (Addison-Wesley), which goes into
much more detail on subjects like pipeline design and artifact management.
In the next chapter, we’ll be going deeper into a topic we touched on briefly here. Namely,
how do we test our microservices to make sure they actually work?
```
[^105]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.226)*

**Verbatim Educational Excerpt** *(Building Microservices, p.226, lines 3–10)*:
```
given service is vital. We’ll want to trigger deployment of a microservice on demand in a
variety of different situations, from deployments locally for dev and test to production
deployments. We’ll also want to keep our deployment mechanisms as similar as possible
from dev to production, as the last thing we want is to find ourselves hitting problems in
production because deployment uses a completely different process!
After many years of working in this space, I am convinced that the most sensible way to
trigger any deployment is via a single, parameterizable command-line call. This can be
triggered by scripts, launched by your CI tool, or typed in by hand. I’ve built wrapper
```
[^106]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.239)*

**Verbatim Educational Excerpt** *(Building Microservices, p.239, lines 2–9)*:
```
When you’re reading the pyramid, the key thing to take away is that as you go up the
pyramid, the test scope increases, as does our confidence that the functionality being
tested works. On the other hand, the feedback cycle time increases as the tests take longer
to run, and when a test fails it can be harder to determine which functionality has broken.
As you go down the pyramid, in general the tests become much faster, so we get much
faster feedback cycles. We find broken functionality faster, our continuous integration
builds are faster, and we are less likely to move on to a new task before finding out we
have broken something. When those smaller-scoped tests fail, we also tend to know what
```
[^107]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Immutable** *(p.209)*

**Verbatim Educational Excerpt** *(Building Microservices, p.209, lines 21–28)*:
```
Another issue is that this option can limit our deployment artifact options. Image-based
deployments are out, as are immutable servers unless you tie multiple different services
together in a single artifact, which we really want to avoid.
The fact that we have multiple services on a single host means that efforts to target scaling
to the service most in need of it can be complicated. Likewise, if one microservice handles
data and operations that are especially sensitive, we might want to set up the underlying
host differently, or perhaps even place the host itself in a separate network segment.
Having everything on one host means we might end up having to treat all services the
```
[^108]
**Annotation:** This excerpt demonstrates 'immutable' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.212)*

**Verbatim Educational Excerpt** *(Building Microservices, p.212, lines 10–17)*:
```
Figure 6-8. A single microservice per host
Just as important is that we have opened up the potential to use alternative deployment
techniques such as image-based deployments or the immutable server pattern, which we
discussed earlier.
We’ve added a lot of complexity in adopting a microservice architecture. The last thing we
want to do is go looking for more sources of complexity. In my opinion, if you don’t have
a viable PaaS available, then this model does a very good job of reducing a system’s
overall complexity. Having a single-service-per-host model is significantly easier to
```
[^109]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Instance** *(p.224)*

**Verbatim Educational Excerpt** *(Building Microservices, p.224, lines 14–21)*:
```
containing its own service, we can host a single VM in Vagrant that runs a Docker
instance. We then use Vagrant to set up and tear down the Docker platform itself, and use
Docker for fast provisioning of individual services.
A number of different technologies are being developed to take advantage of Docker.
CoreOS is a very interesting operating system designed with Docker in mind. It is a
stripped-down Linux OS that provides only the essential services to allow Docker to run.
This means it consumes fewer resources than other operating systems, making it possible
to dedicate even more resources of the underlying machine to our containers. Rather than
```
[^110]
**Annotation:** This excerpt demonstrates 'instance' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **List** *(p.216)*

**Verbatim Educational Excerpt** *(Building Microservices, p.216, lines 3–10)*:
```
good automation. One of our clients in Australia is RealEstate.com.au (REA). Among
other things, the company provides real estate listings for retail and commercial customers
in Australia and elsewhere in the Asia-Pacific region. Over a number of years, it has been
moving its platform toward a distributed, microservices design. When it started on this
journey it had to spend a lot of time getting the tooling around the services just right —
making it easy for developers to provision machines, to deploy their code, or monitor
them. This caused a front-loading of work to get things started.
In the first three months of this exercise, REA was able to move just two new
```
[^111]
**Annotation:** This excerpt demonstrates 'list' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 7: Build** *(pp.243–272)*

This later chapter builds upon the concepts introduced here, particularly: GIL, as, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^112]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Deployment** *(pp.273–312)*

This later chapter builds upon the concepts introduced here, particularly: as, break, def.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^113]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Testing** *(pp.313–350)*

This later chapter builds upon the concepts introduced here, particularly: as, break, def.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^114]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 7: Build

*Source: Building Microservices, 2nd Edition, pages 243–272*

### Chapter Summary
Covers build automation and CI/CD pipeline design for microservices. Discusses continuous integration practices, containerization with Docker, artifact management, versioning strategies, dependency management, and automating the build process for multiple services. [^115]

### Concept-by-Concept Breakdown
#### **Gil** *(p.257)*

**Verbatim Educational Excerpt** *(Building Microservices, p.257, lines 1–8)*:
```
It’s About Conversations
In agile, stories are often referred to as a placeholder for a conversation. CDCs are just
like that. They become the codification of a set of discussions about what a service API
should look like, and when they break, they become a trigger point to have conversations
about how that API should evolve.
It is important to understand that CDCs require good communication and trust between the
consumer and producing service. If both parties are in the same team (or the same
person!), then this shouldn’t be hard. However, if you are consuming a service provided
```
[^116]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.262)*

**Verbatim Educational Excerpt** *(Building Microservices, p.262, lines 1–8)*:
```
Canary Releasing
With canary releasing, we are verifying our newly deployed software by directing
amounts of production traffic against the system to see if it performs as expected.
“Performing as expected” can cover a number of things, both functional and
nonfunctional. For example, we could check that a newly deployed service is responding
to requests within 500ms, or that we see the same proportional error rates from the new
and the old service. But you could go deeper than that. Imagine we’ve released a new
version of the recommendation service. We might run both of them side by side but see if
```
[^117]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 20 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.253)*

**Verbatim Educational Excerpt** *(Building Microservices, p.253, lines 3–10)*:
```
outlined previously? We are trying to ensure that when we deploy a new service to
production, our changes won’t break consumers. One way we can do this without
requiring testing against the real consumer is by using a consumer-driven contract (CDC).
With CDCs, we are defining the expectations of a consumer on a service (or producer).
The expectations of the consumers are captured in code form as tests, which are then run
against the producer. If done right, these CDCs should be run as part of the CI build of the
producer, ensuring that it never gets deployed if it breaks one of these contracts. Very
importantly from a test feedback point of view, these tests need to be run only against a
```
[^118]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.263)*

**Verbatim Educational Excerpt** *(Building Microservices, p.263, lines 2–9)*:
```
So by looking at techniques like blue/green deployment or canary releasing, we find a way
to test closer to (or even in) production, and we also build tools to help us manage a failure
if it occurs. Using these approaches is a tacit acknowledgment that we cannot spot and
catch all problems before we actually release our software.
Sometimes expending the same effort into getting better at remediation of a release can be
significantly more beneficial than adding more automated functional tests. In the web
operations world, this is often referred to as the trade-off between optimizing for mean
time between failures (MTBF) and mean time to repair (MTTR).
```
[^119]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.260)*

**Verbatim Educational Excerpt** *(Building Microservices, p.260, lines 20–27)*:
```
Implementing blue/green deployment requires a few things. First, you need to be able to
direct production traffic to different hosts (or collections of hosts). You could do this by
changing DNS entries, or updating load-balancing configuration. You also need to be able
to provision enough hosts to have both versions of the microservice running at once. If
you’re using an elastic cloud provider, this could be straightforward. Using blue/green
deployments allows you to reduce the risk of deployment, as well as gives you the chance
to revert should you encounter a problem. If you get good at this, the entire process can be
completely automated, with either the full roll-out or revert happening without any human
```
[^120]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.258)*

**Verbatim Educational Excerpt** *(Building Microservices, p.258, lines 16–23)*:
```
Similarly, you may work in an environment where the appetite to learn in production is
low, and people would rather work as hard as they can to eliminate any defects before
production, even if that means software takes longer to ship. As long as you understand
that you cannot be certain that you have eliminated all sources of defects, and that you will
still need to have effective monitoring and remediation in place in production, this may be
a sensible decision.
Obviously you’ll have a better understanding of your own organization’s risk profile than
me, but I would challenge you to think long and hard about how much end-to-end testing
```
[^121]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.248)*

**Verbatim Educational Excerpt** *(Building Microservices, p.248, lines 11–18)*:
```
obvious ownership of these tests, their results get ignored. When they break, everyone
assumes it is someone else’s problem, so they don’t care whether the tests are passing.
Sometimes organizations react by having a dedicated team write these tests. This can be
disastrous. The team developing the software becomes increasingly distant from the tests
for its code. Cycle times increase, as service owners end up waiting for the test team to
write end-to-end tests for the functionality they just wrote. Because another team writes
these tests, the team that wrote the service is less involved with, and therefore less likely
to know, how to run and fix these tests. Although it is unfortunately still a common
```
[^122]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.255)*

**Verbatim Educational Excerpt** *(Building Microservices, p.255, lines 6–13)*:
```
by defining the expectations of the producer using a Ruby DSL. Then, you launch a local
mock server, and run this expectation against it to create the Pact specification file. The
Pact file is just a formal JSON specification; you could obviously handcode these, but
using the language API is much easier. This also gives you a running mock server that can
be used for further isolated tests of the consumer.
Figure 7-11. An overview of how Pact does consumer-driven testing
On the producer side, you then verify that this consumer specification is met by using the
JSON Pact specification to drive calls against your API and verify responses. For this to
```
[^123]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.269)*

**Verbatim Educational Excerpt** *(Building Microservices, p.269, lines 14–20)*:
```
to move old logs out of the way and avoid them taking up all our disk space.
Finally, we might want to monitor the application itself. At a bare minimum, monitoring
the response time of the service is a good idea. You’ll probably be able to do this by
looking at the logs coming either from a web server fronting your service, or perhaps from
the service itself. If we get very advanced, we might want to track the number of errors we
are reporting.
Time passes, loads increase, and we find ourselves needing to scale…
```
[^124]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.253)*

**Verbatim Educational Excerpt** *(Building Microservices, p.253, lines 9–16)*:
```
producer, ensuring that it never gets deployed if it breaks one of these contracts. Very
importantly from a test feedback point of view, these tests need to be run only against a
single producer in isolation, so can be faster and more reliable than the end-to-end tests
they might replace.
As an example, let’s revisit our customer service scenario. The customer service has two
separate consumers: the helpdesk and web shop. Both these consuming services have
expectations for how the customer service will behave. In this example, you create two
sets of tests: one for each consumer representing the helpdesk’s and web shop’s use of the
```
[^125]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.264)*

**Verbatim Educational Excerpt** *(Building Microservices, p.264, lines 1–8)*:
```
Cross-Functional Testing
The bulk of this chapter has been focused on testing specific pieces of functionality, and
how this differs when you are testing a microservice-based system. However, there is
another category of testing that is important to discuss. Nonfunctional requirements is an
umbrella term used to describe those characteristics your system exhibits that cannot
simply be implemented like a normal feature. They include aspects like the acceptable
latency of a web page, the number of users a system should support, how accessible your
user interface should be to people with disabilities, or how secure your customer data
```
[^126]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.257)*

**Verbatim Educational Excerpt** *(Building Microservices, p.257, lines 5–12)*:
```
about how that API should evolve.
It is important to understand that CDCs require good communication and trust between the
consumer and producing service. If both parties are in the same team (or the same
person!), then this shouldn’t be hard. However, if you are consuming a service provided
with a third party, you may not have the frequency of communication, or trust, to make
CDCs work. In these situations, you may have to make do with limited larger-scoped
integration tests just around the untrusted component. Alternatively, if you are creating an
API for thousands of potential consumers, such as with a publicly available web service
```
[^127]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Instance** *(p.243)*

**Verbatim Educational Excerpt** *(Building Microservices, p.243, lines 13–20)*:
```
setting expectations if you want to use it as a mock. You can add or remove these stub
endpoints at will, making it possible for a single Mountebank instance to stub more than
one downstream dependency.
So, if we want to run our service tests for just our customer service we can launch the
customer service, and a Mountebank instance that acts as our loyalty points bank. And if
those tests pass, I can deploy the customer service straightaway! Or can I? What about the
services that call the customer service — the helpdesk and the web shop? Do we know if
we have made a change that may break them? Of course, we have forgotten the important
```
[^128]
**Annotation:** This excerpt demonstrates 'instance' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Json** *(p.255)*

**Verbatim Educational Excerpt** *(Building Microservices, p.255, lines 7–14)*:
```
mock server, and run this expectation against it to create the Pact specification file. The
Pact file is just a formal JSON specification; you could obviously handcode these, but
using the language API is much easier. This also gives you a running mock server that can
be used for further isolated tests of the consumer.
Figure 7-11. An overview of how Pact does consumer-driven testing
On the producer side, you then verify that this consumer specification is met by using the
JSON Pact specification to drive calls against your API and verify responses. For this to
work, the producer codebase needs access to the Pact file. As we discussed earlier in
```
[^129]
**Annotation:** This excerpt demonstrates 'json' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **List** *(p.267)*

**Verbatim Educational Excerpt** *(Building Microservices, p.267, lines 1–8)*:
```
Summary
Bringing this all together, what I have outlined here is a holistic approach to testing that
hopefully gives you some general guidance on how to proceed when testing your own
systems. To reiterate the basics:
Optimize for fast feedback, and separate types of tests accordingly.
Avoid the need for end-to-end tests wherever possible by using consumer-driven
contracts.
Use consumer-driven contracts to provide focus points for conversations between
```
[^130]
**Annotation:** This excerpt demonstrates 'list' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 8: Deployment** *(pp.273–312)*

This later chapter builds upon the concepts introduced here, particularly: as, break, close.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^131]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Testing** *(pp.313–350)*

This later chapter builds upon the concepts introduced here, particularly: as, break, close.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^132]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: From Monitoring to Observability** *(pp.351–386)*

This later chapter builds upon the concepts introduced here, particularly: GIL, as, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^133]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 8: Deployment

*Source: Building Microservices, 2nd Edition, pages 273–312*

### Chapter Summary
Details deployment strategies and infrastructure for microservices including Kubernetes orchestration, cloud platforms, blue-green deployments, canary releases, rolling deployments, infrastructure automation, and managing multiple environments with containers. [^134]

### Concept-by-Concept Breakdown
#### **None** *(p.303)*

**Verbatim Educational Excerpt** *(Building Microservices, p.303, lines 13–15)*:
```
For passwords, you should consider using a technique called salted password hashing.
Badly implemented encryption could be worse than having none, as the false sense of
security (pardon the pun) can lead you to take your eye off the ball.
```
[^135]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.279)*

**Verbatim Educational Excerpt** *(Building Microservices, p.279, lines 1–8)*:
```
Needing to handle tasks like consistently passing through correlation IDs can be a strong
argument for the use of thin shared client wrapper libraries. At a certain scale, it becomes
difficult to ensure that everyone is calling downstream services in the right way and
collecting the right sort of data. It only takes one service partway through the chain to
forget to do this for you to lose critical information. If you do decide to create an in-house
client library to make things like this work out of the box, do make sure you keep it very
thin and not tied to any particular producing service. For example, if you are using HTTP
as the underlying protocol for communication, just wrap a standard HTTP client library,
```
[^136]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.297)*

**Verbatim Educational Excerpt** *(Building Microservices, p.297, lines 1–8)*:
```
HMAC Over HTTP
As we discussed earlier, the use of Basic Authentication over plain HTTP is not terribly
sensible if we are worried about the username and password being compromised. The
traditional alternative is route traffic HTTPS, but there are some downsides. Aside from
managing the certificates, the overhead of HTTPS traffic can place additional strain on
servers (although, to be honest, this has a lower impact than it did several years ago), and
the traffic cannot easily be cached.
An alternative approach, as used extensively by Amazon’s S3 APIs for AWS and in parts
```
[^137]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 24 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.301)*

**Verbatim Educational Excerpt** *(Building Microservices, p.301, lines 9–16)*:
```
schemes allow us to pass in the original principal’s credentials downstream, although with
SAML this is a bit of a nightmare, involving nested SAML assertions that are technically
achievable — but so difficult that no one ever does this. This can become even more
complex, of course. Imagine if the services the online shop talks to in turn make more
downstream calls. How far do we have to go in validating trust for all those deputies?
This problem, unfortunately, has no simple answer, because it isn’t a simple problem. Be
aware that it exists, though. Depending on the sensitivity of the operation in question, you
might have to choose between implicit trust, verifying the identity of the caller, or asking
```
[^138]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.301)*

**Verbatim Educational Excerpt** *(Building Microservices, p.301, lines 9–16)*:
```
schemes allow us to pass in the original principal’s credentials downstream, although with
SAML this is a bit of a nightmare, involving nested SAML assertions that are technically
achievable — but so difficult that no one ever does this. This can become even more
complex, of course. Imagine if the services the online shop talks to in turn make more
downstream calls. How far do we have to go in validating trust for all those deputies?
This problem, unfortunately, has no simple answer, because it isn’t a simple problem. Be
aware that it exists, though. Depending on the sensitivity of the operation in question, you
might have to choose between implicit trust, verifying the identity of the caller, or asking
```
[^139]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.277)*

**Verbatim Educational Excerpt** *(Building Microservices, p.277, lines 14–21)*:
```
initiating request could generate a chain of downstream calls and maybe events being fired
off that are handled in an asynchronous manner. How can we reconstruct the flow of calls
in order to reproduce and fix the problem? Often what we need is to see that error in the
wider context of the initiating call; in other words, we’d like to trace the call chain
upstream, just like we do with a stack trace.
One approach that can be useful here is to use correlation IDs. When the first call is made,
you generate a GUID for the call. This is then passed along to all subsequent calls, as seen
in Figure 8-5, and can be put into your logs in a structured way, much as you’ll already do
```
[^140]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.291)*

**Verbatim Educational Excerpt** *(Building Microservices, p.291, lines 3–10)*:
```
example, it could prevent access to any non-logged-in user to the helpdesk application.
Assuming our gateway can extract attributes about the principal as a result of the
authentication, it may be able to make more nuanced decisions. For example, it is common
to place people in groups, or assign them to roles. We can use this information to
understand what they can do. So for the helpdesk application, we might allow access only
to principals with a specific role (e.g., STAFF). Beyond allowing (or disallowing) access
to specific resources or endpoints, though, we need to leave the rest to the microservice
itself; it will need to make further decisions about what operations to allow.
```
[^141]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.297)*

**Verbatim Educational Excerpt** *(Building Microservices, p.297, lines 31–37)*:
```
the difficulty of getting this stuff right. My colleague was working with a team that was
implementing its own JWT implementation, omitted a single Boolean check, and
invalidated its entire authentication code! Hopefully over time we’ll see more reusable
library implementations.
Finally, understand that this approach ensures only that no third party has manipulated the
request and that the private key itself remains private. The rest of the data in the request
will still be visible to parties snooping on the network.
```
[^142]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.280)*

**Verbatim Educational Excerpt** *(Building Microservices, p.280, lines 13–18)*:
```
and also detect if it is erroring.
As we’ll discuss more in Chapter 11, you can use libraries to implement a circuit breaker
around network calls to help you handle cascading failures in a more elegant fashion,
allowing you to more gracefully degrade your system. Some of these libraries, such as
Hystrix for the JVM, also do a good job of providing these monitoring capabilities for
you.
```
[^143]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.302)*

**Verbatim Educational Excerpt** *(Building Microservices, p.302, lines 3–10)*:
```
everything we can to ensure attackers cannot breach our network, and also that they
cannot breach our applications or operating systems to get access to the underlying close
up. However, we need to be prepared in case they do — defense in depth is key.
Many of the high-profile security breaches involve data at rest being acquired by an
attacker, and that data being readable by the attacker. This is either because the data was
stored in an unencrypted form, or because the mechanism used to protect the data had a
fundamental flaw.
The mechanisms by which secure information can be protected are many and varied, but
```
[^144]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.308)*

**Verbatim Educational Excerpt** *(Building Microservices, p.308, lines 1–4)*:
```
Defense in Depth
As I’ve mentioned earlier, I dislike putting all our eggs in one basket. It’s all about defence
in depth. We’ve talked already about securing data in transit, and securing data at rest. But
are there other protections we could put in place to help?
```
[^145]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.293)*

**Verbatim Educational Excerpt** *(Building Microservices, p.293, lines 5–12)*:
```
ensure security at the perimeter of their networks, and therefore assume they don’t need to
do anything else when two services are talking together. However, should an attacker
penetrate your network, you will have little protection against a typical man-in-the-middle
attack. If the attacker decides to intercept and read the data being sent, change the data
without you knowing, or even in some circumstances pretend to be the thing you are
talking to, you may not know much about it.
This is by far the most common form of inside-perimeter trust I see in organizations. They
may decide to run this traffic over HTTPS, but they don’t do much else. I’m not saying
```
[^146]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.275)*

**Verbatim Educational Excerpt** *(Building Microservices, p.275, lines 25–32)*:
```
line job that inserted a fake event into one of our queues. Our system picked it up and ran
all the various calculations just like any other job, except the results appeared in the junk
book, which was used only for testing. If a re-pricing wasn’t seen within a given time,
Nagios reported this as an issue.
This fake event we created is an example of synthetic transaction. We used this synthetic
transaction to ensure the system was behaving semantically, which is why this technique is
often called semantic monitoring.
In practice, I’ve found the use of synthetic transactions to perform semantic monitoring
```
[^147]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.302)*

**Verbatim Educational Excerpt** *(Building Microservices, p.302, lines 5–11)*:
```
up. However, we need to be prepared in case they do — defense in depth is key.
Many of the high-profile security breaches involve data at rest being acquired by an
attacker, and that data being readable by the attacker. This is either because the data was
stored in an unencrypted form, or because the mechanism used to protect the data had a
fundamental flaw.
The mechanisms by which secure information can be protected are many and varied, but
whichever approach you pick there are some general things to bear in mind.
```
[^148]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.274)*

**Verbatim Educational Excerpt** *(Building Microservices, p.274, lines 21–28)*:
```
expected?
Finally, we can never know what data will be useful! More times than I can count I’ve
wanted to capture data to help me understand something only after the chance to do so has
long passed. I tend to err toward exposing everything and relying on my metrics system to
handle this later.
Libraries exist for a number of different platforms that allow our services to send metrics
to standard systems. Codahale’s Metrics library is one such example library for the JVM.
It allows you to store metrics as counters, timers, or gauges; supports time-boxing metrics
```
[^149]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 9: Testing** *(pp.313–350)*

This later chapter builds upon the concepts introduced here, particularly: as, async, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^150]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, async appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: From Monitoring to Observability** *(pp.351–386)*

This later chapter builds upon the concepts introduced here, particularly: None, as, async.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^151]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Security** *(pp.387–424)*

This later chapter builds upon the concepts introduced here, particularly: None, as, async.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^152]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 9: Testing

*Source: Building Microservices, 2nd Edition, pages 313–350*

### Chapter Summary
Examines testing strategies for microservices including the test pyramid, unit testing, integration testing, contract testing with consumer-driven contracts, end-to-end testing, test automation, and ensuring quality in distributed systems with appropriate test coverage. [^153]

### Concept-by-Concept Breakdown
#### **As** *(p.344)*

**Verbatim Educational Excerpt** *(Building Microservices, p.344, lines 5–12)*:
```
works in reverse, I’ve seen it anecdotally.
Probably the best example was a client I worked with many years ago. Back in the days
when the Web was fairly nascent, and the Internet was seen as something that arrived on
an AOL floppy disk through the door, this company was a large print firm that had a
small, modest website. It had a website because it was the thing to do, but in the grand
scheme of things it was fairly unimportant to how the business operated. When the
original system was created, a fairly arbitrary technical decision was made as to how the
system would work.
```
[^154]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 17 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.343)*

**Verbatim Educational Excerpt** *(Building Microservices, p.343, lines 1–8)*:
```
be asynchronous batch, one of the few cast-iron rules of the very small architecture team.
This coarse-grained communication matches the coarse-grained communication that exists
between the different parts of the business too. By insisting on it being batch, each LOB
has a lot of freedom in how it acts and manages itself. It could afford to take its services
down whenever it wanted, knowing that as long as it can satisfy the batch integration with
other parts of the business and its own business stakeholders, no one would care.
This structure has allowed for significant autonomy of not only the teams but also the
different parts of the business. From a handful of services a few years ago, REA now has
```
[^155]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.322)*

**Verbatim Educational Excerpt** *(Building Microservices, p.322, lines 21–26)*:
```
with security, we’ll see that ignoring the human element can be a grave mistake.
3 In general, key length increases the amount of work required to brute-force-break a key.
Therefore you can assume the longer the key, the more secure your data. However, some
minor concerns have been raised about the implementation of AES-256 for certain types
of keys by respected security expert Bruce Schneier. This is one of those areas where you
need to do more research on what the current advice is at the time of reading!
```
[^156]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.321)*

**Verbatim Educational Excerpt** *(Building Microservices, p.321, lines 4–11)*:
```
attempts. They also sidestep the issue that teams aren’t always able to see the mistakes
they have made themselves, as they are too close to the problem. If you’re a big enough
company, you may have a dedicated infosec team that can help you. If not, find an
external party who can. Reach out to them early, understand how they like to work, and
find out how much notice they need to do a test.
You’ll also need to consider how much verification you require before each release.
Generally, doing a full penetration test, for example, isn’t needed for small incremental
releases, but may be for larger changes. What you need depends on your own risk profile.
```
[^157]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Closure** *(p.348)*

**Verbatim Educational Excerpt** *(Building Microservices, p.348, lines 21–28)*:
```
of machines, there as a sort of exhibit. I noticed a couple of things. First, these servers
weren’t in server enclosures, they were just bare motherboards slotted into the rack. The
main thing I noticed, though, was that the hard drives were attached by velcro. I asked one
of the Googlers why that was. “Oh,” he said, “the hard drives fail so much we don’t want
them screwed in. We just rip them out, throw them in the bin, and velcro in a new one.”
So let me repeat: at scale, even if you buy the best kit, the most expensive hardware, you
cannot avoid the fact that things can and will fail. Therefore, you need to assume failure
can happen. If you build this thinking into everything you do, and plan for failure, you can
```
[^158]
**Annotation:** This excerpt demonstrates 'closure' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.313)*

**Verbatim Educational Excerpt** *(Building Microservices, p.313, lines 14–21)*:
```
This really is basic stuff, but it is surprising how often I see critical software running on
unpatched, old operating systems. You can have the most well-defined and protected
application-level security in the world, but if you have an old version of a web server
running on your machine as root that has an unpatched buffer overflow vulnerability, then
your system could still be extremely vulnerable.
Another thing to look at if you are using Linux is the emergence of security modules for
the operating system itself. AppArmour, for example, allows you to define how your
application is expected to behave, with the kernel keeping an eye on it. If it starts doing
```
[^159]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Dictionary** *(p.323)*

**Verbatim Educational Excerpt** *(Building Microservices, p.323, lines 17–19)*:
```
This statement is often quoted, in various forms, as Conway’s law. Eric S. Raymond
summarized this phenomenon in The New Hacker’s Dictionary (MIT Press) by stating “If
you have four groups working on a compiler, you’ll get a 4-pass compiler.”
```
[^160]
**Annotation:** This excerpt demonstrates 'dictionary' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.345)*

**Verbatim Educational Excerpt** *(Building Microservices, p.345, lines 12–19)*:
```
Likewise, pushing power into development teams to increase autonomy can be fraught.
People who have in the past thrown work over the wall to someone else are accustomed to
having someone else to blame, and may not feel comfortable being fully accountable for
their work. You may even find contractual barriers to having your developers carry
support pagers for the systems they support!
Although this book has mostly been about technology, people are not just a side issue to
be considered; they are the people who built what you have now, and will build what
happens next. Coming up with a vision for how things should be done without considering
```
[^161]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Encoding** *(p.319)*

**Verbatim Educational Excerpt** *(Building Microservices, p.319, lines 3–10)*:
```
crypto. Don’t invent your own security protocols. Unless you are a cryptographic expert
with years of experience, if you try inventing your own encoding or elaborate
cryptographic protections, you will get it wrong. And even if you are a cryptographic
expert, you may still get it wrong.
Many of the tools previously outlined, like AES, are industry-hardened technologies
whose underlying algorithms have been peer reviewed, and whose software
implementation has been rigorously tested and patched over many years. They are good
enough! Reinventing the wheel in many cases is often just a waste of time, but when it
```
[^162]
**Annotation:** This excerpt demonstrates 'encoding' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.321)*

**Verbatim Educational Excerpt** *(Building Microservices, p.321, lines 10–11)*:
```
Generally, doing a full penetration test, for example, isn’t needed for small incremental
releases, but may be for larger changes. What you need depends on your own risk profile.
```
[^163]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.322)*

**Verbatim Educational Excerpt** *(Building Microservices, p.322, lines 8–15)*:
```
get a sense of when to consider security during transit, at rest, or not at all.
Finally, understand the importance of defense in depth, make sure you patch your
operating systems, and even if you consider yourself a rock star, don’t try to implement
your own cryptography!
If you want a general overview of security for browser-based applications, a great place to
start is the excellent Open Web Application Security Project (OWASP) nonprofit, whose
regularly updated Top 10 Security Risk document should be considered essential reading
for any developer. Finally, if you want a more general discussion of cryptography, check
```
[^164]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.327)*

**Verbatim Educational Excerpt** *(Building Microservices, p.327, lines 10–15)*:
```
teams to be self-sufficient.
Netflix learned from this example, and ensured that from the beginning it structured itself
around small, independent teams, so that the services they created would also be
independent from each other. This ensured that the architecture of the system was
optimized for speed of change. Effectively, Netflix designed the organizational structure
for the system architecture it wanted.
```
[^165]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.349)*

**Verbatim Educational Excerpt** *(Building Microservices, p.349, lines 1–8)*:
```
How Much Is Too Much?
We touched on the topic of cross-functional requirements in Chapter 7. Understanding
cross-functional requirements is all about considering aspects like durability of data,
availability of services, throughput, and acceptable latency of services. Many of the
techniques covered in this chapter and elsewhere talk about approaches to implement
these requirements, but only you know exactly what the requirements themselves might
be.
Having an autoscaling system capable of reacting to increased load or failure of individual
```
[^166]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.322)*

**Verbatim Educational Excerpt** *(Building Microservices, p.322, lines 8–15)*:
```
get a sense of when to consider security during transit, at rest, or not at all.
Finally, understand the importance of defense in depth, make sure you patch your
operating systems, and even if you consider yourself a rock star, don’t try to implement
your own cryptography!
If you want a general overview of security for browser-based applications, a great place to
start is the excellent Open Web Application Security Project (OWASP) nonprofit, whose
regularly updated Top 10 Security Risk document should be considered essential reading
for any developer. Finally, if you want a more general discussion of cryptography, check
```
[^167]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Iteration** *(p.343)*

**Verbatim Educational Excerpt** *(Building Microservices, p.343, lines 12–19)*:
```
people there I get the impression that both the architecture and organizational structure as
they stand now are just the latest iteration rather than the destination. I daresay in another
five years REA will look very different again.
Those organizations that are adaptive enough to change not only their system architecture
but also their organizational structure can yield huge benefits in terms of improved
autonomy of teams and faster time to market for new features and functionality. REA is
just one of a number of organizations that are realizing that system architecture doesn’t
exist in a vacuum.
```
[^168]
**Annotation:** This excerpt demonstrates 'iteration' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 10: From Monitoring to Observability** *(pp.351–386)*

This later chapter builds upon the concepts introduced here, particularly: as, async, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^169]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, async appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Security** *(pp.387–424)*

This later chapter builds upon the concepts introduced here, particularly: as, async, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^170]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, async appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 12: Resiliency** *(pp.425–448)*

This later chapter builds upon the concepts introduced here, particularly: as, async, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^171]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, async appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 10: From Monitoring to Observability

*Source: Building Microservices, 2nd Edition, pages 351–386*

### Chapter Summary
Explores observability and monitoring in microservices environments. Covers metrics collection, centralized logging, distributed tracing, alerting strategies, building dashboards, implementing telemetry, health checks, and defining SLOs and SLAs for service reliability. [^172]

### Concept-by-Concept Breakdown
#### **Gil** *(p.354)*

**Verbatim Educational Excerpt** *(Building Microservices, p.354, lines 1–8)*:
```
The Antifragile Organization
In his book Antifragile (Random House), Nassim Taleb talks about things that actually
benefit from failure and disorder. Ariel Tseitlin used this concept to coin the concept of the
antifragile organization in regards to how Netflix operates.
The scale at which Netflix operates is well known, as is the fact that Netflix is based
entirely on the AWS infrastructure. These two factors mean that it has to embrace failure
well. Netflix goes beyond that by actually inciting failure to ensure that its systems are
tolerant of it.
```
[^173]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.365)*

**Verbatim Educational Excerpt** *(Building Microservices, p.365, lines 9–12)*:
```
written to take advantage of them. The other problem is that this form of scaling may not
do much to improve our server’s resiliency if we only have one of them! Nonetheless, this
can be a good quick win, especially if you’re using a virtualization provider that lets you
resize machines easily.
```
[^174]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.360)*

**Verbatim Educational Excerpt** *(Building Microservices, p.360, lines 1–8)*:
```
library is a JVM circuit breaker abstraction that comes with some powerful monitoring,
but other implementations exist for different technology stacks, such as Polly for .NET, or
the circuit_breaker mixin for Ruby.
In many ways, bulkheads are the most important of these three patterns. Timeouts and
circuit breakers help you free up resources when they are becoming constrained, but
bulkheads can ensure they don’t become constrained in the first place. Hystrix allows you,
for example, to implement bulkheads that actually reject requests in certain conditions to
ensure that resources don’t become even more saturated; this is known as load shedding.
```
[^175]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.375)*

**Verbatim Educational Excerpt** *(Building Microservices, p.375, lines 1–8)*:
```
Scaling for Writes
Reads are comparatively easy to scale. What about writes? One approach is to use
sharding. With sharding, you have multiple database nodes. You take a piece of data to be
written, apply some hashing function to the key of the data, and based on the result of the
function learn where to send the data. To pick a very simplistic (and actually bad)
example, imagine that customer records A–M go to one database instance, and N–Z
another. You can manage this yourself in your application, but some databases, like
Mongo, handle much of it for you.
```
[^176]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 24 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.384)*

**Verbatim Educational Excerpt** *(Building Microservices, p.384, lines 11–18)*:
```
One way to protect the origin in such a situation is never to allow requests to go to the
origin in the first place. Instead, the origin itself populates the cache asynchronously when
needed, as shown in Figure 11-7. If a cache miss is caused, this triggers an event that the
origin can pick up on, alerting it that it needs to repopulate the cache. So if an entire shard
has vanished, we can rebuild the cache in the background. We could decide to block the
original request waiting for the region to be repopulated, but this could cause contention
on the cache itself, leading to further problems. It’s more likely if we are prioritizing
keeping the system stable that we would fail the original request, but it would fail fast.
```
[^177]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.357)*

**Verbatim Educational Excerpt** *(Building Microservices, p.357, lines 1–8)*:
```
Circuit Breakers
In your own home, circuit breakers exist to protect your electrical devices from spikes in
the power. If a spike occurs, the circuit breaker gets blown, protecting your expensive
home appliances. You can also manually disable a circuit breaker to cut the power to part
of your home, allowing you to work safely on the electrics. Michael Nygard’s book
Release It! (Pragmatic Programmers) shows how the same idea can work wonders as a
protection mechanism for our software.
Consider the story I shared just a moment ago. The downstream legacy ad application was
```
[^178]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 14 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.352)*

**Verbatim Educational Excerpt** *(Building Microservices, p.352, lines 8–15)*:
```
outline the sort of thing that can go wrong.
I was a technical lead on a project where we were building an online classified ads
website. The website itself handled fairly high volumes, and generated a good deal of
income for the business. Our core application handled some display of classified ads itself,
and also proxied calls to other services that provided different types of products, as shown
in Figure 11-1. This is actually an example of a strangler application, where a new system
intercepts calls made to legacy applications and gradually replaces them altogether. As
part of this project, we were partway through retiring the older applications. We had just
```
[^179]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.351)*

**Verbatim Educational Excerpt** *(Building Microservices, p.351, lines 19–26)*:
```
we understand the business context we won’t understand what action we should be taking.
For example, perhaps we close the entire site, still allow people to browse the catalog of
items, or replace the part of the UI containing the cart control with a phone number for
placing an order. But for every customer-facing interface that uses multiple microservices,
or every microservice that depends on multiple downstream collaborators, you need to ask
yourself, “What happens if this is down?” and know what to do.
By thinking about the criticality of each of our capabilities in terms of our cross-functional
requirements, we’ll be much better positioned to know what we can do. Now let’s
```
[^180]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.353)*

**Verbatim Educational Excerpt** *(Building Microservices, p.353, lines 20–27)*:
```
requests themselves hung. It turned out the connection pool library we were using did
have a timeout for waiting for workers, but this was disabled by default! This led to a huge
build-up of blocked threads. Our application normally had 40 concurrent connections at
any given time. In the space of five minutes, this situation caused us to peak at around 800
connections, bringing the system down.
What was worse was that the downstream service we were talking to represented
functionality that less than 5% of our customer base used, and generated even less revenue
than that. When you get down to it, we discovered the hard way that systems that just act
```
[^181]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.353)*

**Verbatim Educational Excerpt** *(Building Microservices, p.353, lines 31–38)*:
```
HTTP connection pool for all outbound requests. This meant that one slow service could
exhaust the number of available workers all by itself, even if everything else was healthy.
Lastly, it was clear that the downstream service in question wasn’t healthy, but we kept
sending traffic its way. In our situation, this meant we were actually making a bad
situation worse, as the downstream service had no chance to recover. We ended up
implementing three fixes to avoid this happening again: getting our timeouts right,
implementing bulkheads to separate out different connection pools, and implementing a
circuit breaker to avoid sending calls to an unhealthy system in the first place.
```
[^182]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.373)*

**Verbatim Educational Excerpt** *(Building Microservices, p.373, lines 5–11)*:
```
For example, I could store a copy of all data written to my database in a resilient
filesystem. If the database goes down, my data isn’t lost, as I have a copy, but the database
itself isn’t available, which may make my microservice unavailable too. A more common
model would be using a standby. All data written to the primary database gets copied to
the standby replica database. If the primary goes down, my data is safe, but without a
mechanism to either bring it back up or promote the replica to the primary, we don’t have
an available database, even though our data is safe.
```
[^183]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.359)*

**Verbatim Educational Excerpt** *(Building Microservices, p.359, lines 1–8)*:
```
Bulkheads
In another pattern from Release It!, Nygard introduces the concept of a bulkhead as a way
to isolate yourself from failure. In shipping, a bulkhead is a part of the ship that can be
sealed off to protect the rest of the ship. So if the ship springs a leak, you can close the
bulkhead doors. You lose part of the ship, but the rest of it remains intact.
In software architecture terms, there are lots of different bulkheads we can consider.
Returning to my own experience, we actually missed the chance to implement a bulkhead.
We should have used different connection pools for each downstream connection. That
```
[^184]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.351)*

**Verbatim Educational Excerpt** *(Building Microservices, p.351, lines 1–8)*:
```
Degrading Functionality
An essential part of building a resilient system, especially when your functionality is
spread over a number of different microservices that may be up or down, is the ability to
safely degrade functionality. Let’s imagine a standard web page on our ecommerce site. To
pull together the various parts of that website, we might need several microservices to play
a part. One microservice might display the details about the album being offered for sale.
Another might show the price and stock level. And we’ll probably be showing shopping
cart contents too, which may be yet another microservice. Now if one of those services is
```
[^185]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.354)*

**Verbatim Educational Excerpt** *(Building Microservices, p.354, lines 26–33)*:
```
Embracing and inciting failure through software, and building systems that can handle it,
is only part of what Netflix does. It also understands the importance of learning from the
failure when it occurs, and adopting a blameless culture when mistakes do happen.
Developers are further empowered to be part of this learning and evolving process, as each
developer is also responsible for managing his or her production services.
By causing failure to happen, and building for it, Netflix has ensured that the systems it
has scale better, and better support the needs of its customers.
Not everyone needs to go to the sorts of extremes that Google or Netflix do, but it is
```
[^186]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Instance** *(p.368)*

**Verbatim Educational Excerpt** *(Building Microservices, p.368, lines 3–10)*:
```
a typical microservice that exposes a synchronous HTTP endpoint, the easiest way to
achieve this is to have multiple hosts running your microservice instance, sitting behind a
load balancer, as shown in Figure 11-4. To consumers of the microservice, you don’t know
if you are talking to one microservice instance or a hundred.
Figure 11-4. An example of a load balancing approach to scale the number of customer service instances
Load balancers come in all shapes and sizes, from big and expensive hardware appliances
to software-based load balancers like mod_proxy. They all share some key capabilities.
They distribute calls sent to them to one or more instances based on some algorithm,
```
[^187]
**Annotation:** This excerpt demonstrates 'instance' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 11: Security** *(pp.387–424)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^188]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 12: Resiliency** *(pp.425–448)*

This later chapter builds upon the concepts introduced here, particularly: GIL, as, async.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^189]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 13: Scaling** *(pp.449–464)*

This later chapter builds upon the concepts introduced here, particularly: as, async, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^190]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, async appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 11: Security

*Source: Building Microservices, 2nd Edition, pages 387–424*

### Chapter Summary
Addresses security concerns in microservices including authentication and authorization mechanisms, OAuth and JWT tokens, encryption and TLS/SSL, API security best practices, secret management, identity management, and implementing defense-in-depth security strategies. [^191]

### Concept-by-Concept Breakdown
#### **Gil** *(p.422)*

**Verbatim Educational Excerpt** *(Building Microservices, p.422, lines 8–15)*:
```
aggregated logs, Logs, Logs, and Yet More Logs…
antifragile systems, Microservices, The Antifragile Organization-Isolation
bulkheads, Bulkheads
circuit breakers, Circuit Breakers
examples of, The Antifragile Organization
increased use of, Microservices
isolation, Isolation
load shedding, Bulkheads
```
[^192]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.410)*

**Verbatim Educational Excerpt** *(Building Microservices, p.410, lines 3–10)*:
```
notable experiences to draw upon, I’m sure the next few years will yield more useful
patterns in handling them at scale. Nonetheless, I hope this chapter has outlined some
steps you can take on your journey to microservices at scale that will hold you in good
stead.
In addition to what I have covered here, I recommend Michael Nygard’s excellent book
Release It!. In it he shares a collection of stories about system failure and some patterns to
help deal with it well. The book is well worth a read (in fact, I would go so far as to say it
should be considered essential reading for anyone building systems at scale).
```
[^193]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.418)*

**Verbatim Educational Excerpt** *(Building Microservices, p.418, lines 7–14)*:
```
different sorts of failure mode. So make sure if you’re using client libraries that the
abstraction of the remote call doesn’t go too far.
If we hold the tenets of antifragility in mind, and expect failure will occur anywhere and
everywhere, we are on the right track. Make sure your timeouts are set appropriately.
Understand when and how to use bulkheads and circuit breakers to limit the fallout of a
failing component. Understand what the customer-facing impact will be if only one part of
the system is misbehaving. Know what the implications of a network partition might be,
and whether sacrificing availability or consistency in a given situation is the right call.
```
[^194]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.401)*

**Verbatim Educational Excerpt** *(Building Microservices, p.401, lines 2–9)*:
```
Zookeeper was originally developed as part of the Hadoop project. It is used for an almost
bewildering array of use cases, including configuration management, synchronizing data
between services, leader election, message queues, and (usefully for us) as a naming
service.
Like many similar types of systems, Zookeeper relies on running a number of nodes in a
cluster to provide various guarantees. This means you should expect to be running at least
three Zookeeper nodes. Most of the smarts in Zookeeper are around ensuring that data is
replicated safely between these nodes, and that things remain consistent when nodes fail.
```
[^195]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.401)*

**Verbatim Educational Excerpt** *(Building Microservices, p.401, lines 1–8)*:
```
Zookeeper
Zookeeper was originally developed as part of the Hadoop project. It is used for an almost
bewildering array of use cases, including configuration management, synchronizing data
between services, leader election, message queues, and (usefully for us) as a naming
service.
Like many similar types of systems, Zookeeper relies on running a number of nodes in a
cluster to provide various guarantees. This means you should expect to be running at least
three Zookeeper nodes. Most of the smarts in Zookeeper are around ensuring that data is
```
[^196]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 17 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.423)*

**Verbatim Educational Excerpt** *(Building Microservices, p.423, lines 10–17)*:
```
platform-specific, Platform-Specific Artifacts
asynchronous collaboration
complexities of, Complexities of Asynchronous Architectures
implementing, Implementing Asynchronous Event-Based Collaboration
vs. synchronous, Synchronous Versus Asynchronous
ATOM specification, Technology Choices
authentication/authorization, Authentication and Authorization-The Deputy
Problem
```
[^197]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.417)*

**Verbatim Educational Excerpt** *(Building Microservices, p.417, lines 2–9)*:
```
We should always strive to ensure that our microservices can and are deployed by
themselves. Even when breaking changes are required, we should seek to coexist
versioned endpoints to allow our consumers to change over time. This allows us to
optimize for speed of release of new features, as well as increasing the autonomy of the
teams owning these microservices by ensuring that they don’t have to constantly
orchestrate their deployments. When using RPC-based integration, avoid tightly bound
client/server stub generation such as that promoted by Java RMI.
By adopting a one-service-per-host model, you reduce side effects that could cause
```
[^198]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.408)*

**Verbatim Educational Excerpt** *(Building Microservices, p.408, lines 12–19)*:
```
execute calls against the service itself. Executing calls isn’t quite as slick, though.
Whereas with Swagger you can define templates to do things like issue a POST request,
with HAL you’re more on your own. The flipside to this is that the inherent power of
hypermedia controls lets you much more effectively explore the API exposed by the
service, as you can follow links around very easily. It turns out that web browsers are
pretty good at that sort of thing!
Unlike with Swagger, all the information needed to drive this documentation and sandbox
is embedded in the hypermedia controls. This is a double-edged sword. If you are already
```
[^199]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.392)*

**Verbatim Educational Excerpt** *(Building Microservices, p.392, lines 1–8)*:
```
Sacrificing Availability
What happens if we need to keep consistency and want to drop something else instead?
Well, to keep consistency, each database node needs to know the copy of the data it has is
the same as the other database node. Now in the partition, if the database nodes can’t talk
to each other, they cannot coordinate to ensure consistency. We are unable to guarantee
consistency, so our only option is to refuse to respond to the request. In other words, we
have sacrificed availability. Our system is consistent and partition tolerant, or CP. In this
mode our service would have to work out how to degrade functionality until the partition
```
[^200]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.417)*

**Verbatim Educational Excerpt** *(Building Microservices, p.417, lines 13–17)*:
```
they happen.
Remember that it should be the norm, not the exception, that you can make a change to a
single service and release it into production, without having to deploy any other services
in lock-step. Your consumers should decide when they update themselves, and you need to
accommodate this.
```
[^201]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.417)*

**Verbatim Educational Excerpt** *(Building Microservices, p.417, lines 13–17)*:
```
they happen.
Remember that it should be the norm, not the exception, that you can make a change to a
single service and release it into production, without having to deploy any other services
in lock-step. Your consumers should decide when they update themselves, and you need to
accommodate this.
```
[^202]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.407)*

**Verbatim Educational Excerpt** *(Building Microservices, p.407, lines 5–12)*:
```
clear what sort of content the server expects.
To do all of this, Swagger needs the service to expose a sidecar file matching the Swagger
format. Swagger has a number of libraries for different languages that does this for you.
For example, for Java you can annotate methods that match your API calls, and the file
gets generated for you.
I like the end-user experience that Swagger gives you, but it does little for the incremental
exploration concept at the heart of hypermedia. Still, it’s a pretty nice way to expose
documentation about your services.
```
[^203]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.398)*

**Verbatim Educational Excerpt** *(Building Microservices, p.398, lines 17–24)*:
```
and entries, this could be quite a neat solution, but it is a lot of work if you aren’t getting
other benefits from this setup.
DNS has a host of advantages, the main one being it is such a well-understood and well-
used standard that almost any technology stack will support it. Unfortunately, while a
number of services exist for managing DNS inside an organization, few of them seem
designed for an environment where we are dealing with highly disposable hosts, making
updating DNS entries somewhat painful. Amazon’s Route53 service does a pretty good
job of this, but I haven’t seen a self-hosted option that is as good yet, although (as we’ll
```
[^204]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.392)*

**Verbatim Educational Excerpt** *(Building Microservices, p.392, lines 7–14)*:
```
have sacrificed availability. Our system is consistent and partition tolerant, or CP. In this
mode our service would have to work out how to degrade functionality until the partition
is healed and the database nodes can be resynchronized.
Consistency across multiple nodes is really hard. There are few things (perhaps nothing)
harder in distributed systems. Think about it for a moment. Imagine I want to read a
record from the local database node. How do I know it is up to date? I have to go and ask
the other node. But I also have to ask that database node to not allow it to be updated
while the read completes; in other words, I need to initiate a transactional read across
```
[^205]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **General-Purpose** *(p.403)*

**Verbatim Educational Excerpt** *(Building Microservices, p.403, lines 2–9)*:
```
Netflix’s open source Eureka system bucks the trend of systems like Consul and
Zookeeper in that it doesn’t also try to be a general-purpose configuration store. It is
actually very targeted in its use case.
Eureka also provides basic load-balancing capabilities in that it can support basic round-
robin lookup of service instances. It provides a REST-based endpoint so you can write
your own clients, or you can use its own Java client. The Java client provides additional
capabilities, such as health checking of instances. Obviously if you bypass Eureka’s own
client and go directly to the REST endpoint, you’re on your own there.
```
[^206]
**Annotation:** This excerpt demonstrates 'general-purpose' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 12: Resiliency** *(pp.425–448)*

This later chapter builds upon the concepts introduced here, particularly: GIL, as, async.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^207]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 13: Scaling** *(pp.449–464)*

This later chapter builds upon the concepts introduced here, particularly: as, async, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^208]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, async appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 14: User Interfaces** *(pp.465–472)*

This later chapter builds upon the concepts introduced here, particularly: GIL, as, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^209]

**Annotation:** Forward reference: Chapter 14 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 12: Resiliency

*Source: Building Microservices, 2nd Edition, pages 425–448*

### Chapter Summary
Focuses on building resilient microservices with fault tolerance patterns including circuit breakers, retry policies, timeouts, bulkhead pattern, graceful degradation, failure handling strategies, chaos engineering practices, and designing for redundancy and high availability. [^210]

### Concept-by-Concept Breakdown
#### **Gil** *(p.426)*

**Verbatim Educational Excerpt** *(Building Microservices, p.426, lines 10–17)*:
```
certificate management, Client Certificates
Chaos Gorilla, The Antifragile Organization
Chaos Monkey, The Antifragile Organization
choreographed architecture, Orchestration Versus Choreography
circuit breakers, Tailored Service Template, Circuit Breakers
circuit_breaker mixin for Ruby, Bulkheads
class-responsibility-collaboration (CRC), Cost of Change
client certificates, Client Certificates
```
[^211]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.430)*

**Verbatim Educational Excerpt** *(Building Microservices, p.430, lines 1–8)*:
```
refactoring databases, Staging the Break
selecting separation points, Getting to Grips with the Problem
selecting separation timing, Understanding Root Causes
shared data, Example: Shared Data
shared static data, Example: Shared Static Data
shared tables, Example: Shared Tables
transactional boundaries, Transactional Boundaries
database integration, The Shared Database
```
[^212]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.427)*

**Verbatim Educational Excerpt** *(Building Microservices, p.427, lines 2–9)*:
```
collaboration, Summary
event-based, Synchronous Versus Asynchronous
request/response, Synchronous Versus Asynchronous
Command-Query Responsibility Segregation (CQRS), CQRS
commits, two-phase, Distributed Transactions
communication
adapting to pathways, Adapting to Communication Pathways
protocols for (SOAP), What About Service-Oriented Architecture?
```
[^213]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.425)*

**Verbatim Educational Excerpt** *(Building Microservices, p.425, lines 1–8)*:
```
Brakeman, Baking Security In
breaking changes
avoiding, Avoid Breaking Changes
deferring, Defer It for as Long as Possible
early detection of, Catch Breaking Changes Early
brittle tests, Flaky and Brittle Tests
brittleness, Brittleness
build pipelines, Build Pipelines and Continuous Delivery
```
[^214]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.426)*

**Verbatim Educational Excerpt** *(Building Microservices, p.426, lines 15–22)*:
```
circuit_breaker mixin for Ruby, Bulkheads
class-responsibility-collaboration (CRC), Cost of Change
client certificates, Client Certificates
client libraries, Client Libraries
client-side caching, Client-Side, Proxy, and Server-Side Caching
code reuse, DRY and the Perils of Code Reuse in a Microservice World
coding architect, Zoning
cohesion, Small, and Focused on Doing One Thing Well, High Cohesion
```
[^215]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.425)*

**Verbatim Educational Excerpt** *(Building Microservices, p.425, lines 3–10)*:
```
avoiding, Avoid Breaking Changes
deferring, Defer It for as Long as Possible
early detection of, Catch Breaking Changes Early
brittle tests, Flaky and Brittle Tests
brittleness, Brittleness
build pipelines, Build Pipelines and Continuous Delivery
bulkheads, Bulkheads
bundled service release, And the Inevitable Exceptions
```
[^216]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.438)*

**Verbatim Educational Excerpt** *(Building Microservices, p.438, lines 20–24)*:
```
J
JSON, JSON, XML, or Something Else?
JSON web tokens (JWT), HMAC Over HTTP
K
Karyon, Tailored Service Template
```
[^217]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.435)*

**Verbatim Educational Excerpt** *(Building Microservices, p.435, lines 2–9)*:
```
evolutionary architects (see systems architects)
exception handling, Exception Handling
exemplars, Exemplars
exploratory testing, Types of Tests
F
failure bots, The Antifragile Organization
failures
cascading, The Cascade
```
[^218]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.435)*

**Verbatim Educational Excerpt** *(Building Microservices, p.435, lines 2–9)*:
```
evolutionary architects (see systems architects)
exception handling, Exception Handling
exemplars, Exemplars
exploratory testing, Types of Tests
F
failure bots, The Antifragile Organization
failures
cascading, The Cascade
```
[^219]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.432)*

**Verbatim Educational Excerpt** *(Building Microservices, p.432, lines 6–13)*:
```
overview of, Summary
separating from release, Separating Deployment from Release
service configuration, Service Configuration
virtualization approach, From Physical to Virtual
virtualization, hypervisors, Traditional Virtualization
virtualization, traditional, Traditional Virtualization
virtualization, type 2, Traditional Virtualization
deputy problem, The Deputy Problem
```
[^220]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.441)*

**Verbatim Educational Excerpt** *(Building Microservices, p.441, lines 16–23)*:
```
CAP theorem, CAP Theorem
cross-functional requirements (CFR), How Much Is Too Much?
dealing with failures, Failure Is Everywhere
degrading functionality, Degrading Functionality
documenting services, Documenting Services
dynamic service registries, Dynamic Service Registries
idempotent operations, Idempotency
scaling, Scaling
```
[^221]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Immutable** *(p.432)*

**Verbatim Educational Excerpt** *(Building Microservices, p.432, lines 2–9)*:
```
environments to consider, Environments
immutable servers, Immutable Servers
interfaces, A Deployment Interface
microservices vs. monolithic systems, Ease of Deployment, Deployment
overview of, Summary
separating from release, Separating Deployment from Release
service configuration, Service Configuration
virtualization approach, From Physical to Virtual
```
[^222]
**Annotation:** This excerpt demonstrates 'immutable' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.433)*

**Verbatim Educational Excerpt** *(Building Microservices, p.433, lines 6–13)*:
```
HAL (Hypertext Application Language), HAL and the HAL Browser
importance of, Documenting Services
self-describing systems, HAL and the HAL Browser
Swagger, Swagger
domain-driven design, Microservices
Dropwizard, Tailored Service Template
DRY (Don’t Repeat Yourself), DRY and the Perils of Code Reuse in a
Microservice World
```
[^223]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Json** *(p.438)*

**Verbatim Educational Excerpt** *(Building Microservices, p.438, lines 20–24)*:
```
J
JSON, JSON, XML, or Something Else?
JSON web tokens (JWT), HMAC Over HTTP
K
Karyon, Tailored Service Template
```
[^224]
**Annotation:** This excerpt demonstrates 'json' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **List** *(p.428)*

**Verbatim Educational Excerpt** *(Building Microservices, p.428, lines 5–12)*:
```
basics, A Brief Introduction to Continuous Integration
checklist for, Are You Really Doing It?
mapping to microservices, Mapping Continuous Integration to
Microservices
Conway’s law
evidence of, Evidence
in reverse, Conway’s Law in Reverse
statement of, Conway’s Law and System Design
```
[^225]
**Annotation:** This excerpt demonstrates 'list' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 13: Scaling** *(pp.449–464)*

This later chapter builds upon the concepts introduced here, particularly: as, async, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^226]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, async appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 14: User Interfaces** *(pp.465–472)*

This later chapter builds upon the concepts introduced here, particularly: GIL, as, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^227]

**Annotation:** Forward reference: Chapter 14 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 13: Scaling

*Source: Building Microservices, 2nd Edition, pages 449–464*

### Chapter Summary
Covers scaling strategies for microservices including horizontal and vertical scaling, load balancing techniques, caching strategies, performance optimization, autoscaling mechanisms, capacity planning, data partitioning and sharding, and achieving elasticity in distributed systems. [^228]

### Concept-by-Concept Breakdown
#### **As** *(p.460)*

**Verbatim Educational Excerpt** *(Building Microservices, p.460, lines 3–10)*:
```
20,000 known species of bees, only seven are considered honey bees. They are distinct
because they produce and store honey, as well as building hives from wax. Beekeeping to
collect honey has been a human pursuit for thousands of years.
Honey bees live in hives with thousands of individuals and have a very organized social
structure. There are three castes: queen, drone, and worker. Each hive has one queen, who
remains fertile for 3–5 years after her mating flight, and lays up to 2,000 eggs per day.
Drones are male bees who mate with the queen (and die in the act because of their barbed
sex organs). Worker bees are sterile females who fill many roles during their lifetime, such
```
[^229]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 13 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.464)*

**Verbatim Educational Excerpt** *(Building Microservices, p.464, lines 5–12)*:
```
Downsides to REST Over HTTP
Implementing Asynchronous Event-Based Collaboration
Technology Choices
Complexities of Asynchronous Architectures
Services as State Machines
Reactive Extensions
DRY and the Perils of Code Reuse in a Microservice World
Client Libraries
```
[^230]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.457)*

**Verbatim Educational Excerpt** *(Building Microservices, p.457, lines 7–14)*:
```
versioning, Versioning-Use Multiple Concurrent Service Versions
catching breaking changes early, Catch Breaking Changes Early
coexisting different endpoints, Coexist Different Endpoints
deferring breaking changes, Defer It for as Long as Possible
multiple concurrent versions, Use Multiple Concurrent Service Versions
semantic, Use Semantic Versioning
vertical scaling, Go Bigger
virtual private clouds (VPC), Network Segregation
```
[^231]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.457)*

**Verbatim Educational Excerpt** *(Building Microservices, p.457, lines 9–16)*:
```
coexisting different endpoints, Coexist Different Endpoints
deferring breaking changes, Defer It for as Long as Possible
multiple concurrent versions, Use Multiple Concurrent Service Versions
semantic, Use Semantic Versioning
vertical scaling, Go Bigger
virtual private clouds (VPC), Network Segregation
virtualization
hypervisors, Traditional Virtualization
```
[^232]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.458)*

**Verbatim Educational Excerpt** *(Building Microservices, p.458, lines 6–11)*:
```
X
XML, JSON, XML, or Something Else?
Z
Zed Attack Proxy (ZAP), Baking Security In
Zipkin, Correlation IDs
Zookeeper, Zookeeper
```
[^233]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.453)*

**Verbatim Educational Excerpt** *(Building Microservices, p.453, lines 14–21)*:
```
decision-making guidelines for, A Principled Approach
exception handling, Exception Handling
governance, Governance and Leading from the Center
responsibilities of, Inaccurate Comparisons, Technical Debt, Summary
role of, An Evolutionary Vision for the Architect
service boundaries and, Zoning
standards enforcement by, Governance Through Code-Tailored Service
Template
```
[^234]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.453)*

**Verbatim Educational Excerpt** *(Building Microservices, p.453, lines 14–21)*:
```
decision-making guidelines for, A Principled Approach
exception handling, Exception Handling
governance, Governance and Leading from the Center
responsibilities of, Inaccurate Comparisons, Technical Debt, Summary
role of, An Evolutionary Vision for the Architect
service boundaries and, Zoning
standards enforcement by, Governance Through Code-Tailored Service
Template
```
[^235]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.455)*

**Verbatim Educational Excerpt** *(Building Microservices, p.455, lines 8–15)*:
```
semantic monitoring, So Should You Use End-to-End Tests?
separating deployment from release, Separating Deployment from
Release
service test implementation, Implementing Service Tests
types of tests, Types of Tests
third-party software, Integrating with Third-Party Software-The Strangler
Pattern, Data Retrieval via Service Calls
building vs. buying, Integrating with Third-Party Software
```
[^236]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.454)*

**Verbatim Educational Excerpt** *(Building Microservices, p.454, lines 21–23)*:
```
consumer-driven tests, Consumer-Driven Tests to the Rescue
cross-functional, Cross-Functional Testing
end-to-end tests, Those Tricky End-to-End Tests
```
[^237]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.452)*

**Verbatim Educational Excerpt** *(Building Microservices, p.452, lines 2–9)*:
```
architectural safety, Architectural Safety
importance of, The Required Standard
interfaces, Interfaces
monitoring, Monitoring
static data, Example: Shared Static Data
Strangler Application Pattern, The Strangler Pattern, Architectural Safety
Measures
strategic goals
```
[^238]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Json** *(p.458)*

**Verbatim Educational Excerpt** *(Building Microservices, p.458, lines 6–11)*:
```
X
XML, JSON, XML, or Something Else?
Z
Zed Attack Proxy (ZAP), Baking Security In
Zipkin, Correlation IDs
Zookeeper, Zookeeper
```
[^239]
**Annotation:** This excerpt demonstrates 'json' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Mock** *(p.450)*

**Verbatim Educational Excerpt** *(Building Microservices, p.450, lines 6–13)*:
```
implementation of, Implementing Service Tests
mocking vs. stubbing, Mocking or Stubbing
Mountebank server for, A Smarter Stub Service
scope of, Service Tests
service-oriented architectures (SOA)
concept of, What About Service-Oriented Architecture?
drawbacks of, What About Service-Oriented Architecture?
reuse of functionality in, Composability
```
[^240]
**Annotation:** This excerpt demonstrates 'mock' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Module** *(p.461)*

**Verbatim Educational Excerpt** *(Building Microservices, p.461, lines 24–26)*:
```
Shared Libraries
Modules
No Silver Bullet
```
[^241]
**Annotation:** This excerpt demonstrates 'module' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Open** *(p.451)*

**Verbatim Educational Excerpt** *(Building Microservices, p.451, lines 4–11)*:
```
man-in-the-middle attacks, Allow Everything Inside the Perimeter
SAML/OpenID Connect, Use SAML or OpenID Connect
sharding, Scaling for Writes
shared code, DRY and the Perils of Code Reuse in a Microservice World
shared data, Example: Shared Data
shared libraries, Shared Libraries
shared models, Shared and Hidden Models
shared static data, Example: Shared Static Data
```
[^242]
**Annotation:** This excerpt demonstrates 'open' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Pass** *(p.449)*

**Verbatim Educational Excerpt** *(Building Microservices, p.449, lines 1–8)*:
```
overview of, Summary
passwords, Go with the Well Known
privacy issues, Be Frugal
securing data at rest, Securing Data at Rest
service-to-service authentication/authorization, Service-to-Service
Authentication and Authorization
tool selection, The Golden Rule
virtual private clouds, Network Segregation
```
[^243]
**Annotation:** This excerpt demonstrates 'pass' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 14: User Interfaces** *(pp.465–472)*

This later chapter builds upon the concepts introduced here, particularly: as, break, def.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^244]

**Annotation:** Forward reference: Chapter 14 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 14: User Interfaces

*Source: Building Microservices, 2nd Edition, pages 465–472*

### Chapter Summary
Examines user interface patterns for microservices including micro frontends, backend for frontend (BFF) pattern, API composition techniques, GraphQL for client queries, single-page applications (SPA), UI aggregation strategies, and designing frontend architectures for microservices. [^245]

### Concept-by-Concept Breakdown
#### **Gil** *(p.471)*

**Verbatim Educational Excerpt** *(Building Microservices, p.471, lines 15–22)*:
```
Architectural Safety Measures
The Antifragile Organization
Timeouts
Circuit Breakers
Bulkheads
Isolation
Idempotency
Scaling
```
[^246]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.472)*

**Verbatim Educational Excerpt** *(Building Microservices, p.472, lines 1–8)*:
```
Worker-Based Systems
Starting Again
Scaling Databases
Availability of Service Versus Durability of Data
Scaling for Reads
Scaling for Writes
Shared Database Infrastructure
CQRS
```
[^247]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.465)*

**Verbatim Educational Excerpt** *(Building Microservices, p.465, lines 9–16)*:
```
It’s All About Seams
Breaking Apart MusicCorp
The Reasons to Split the Monolith
Pace of Change
Team Structure
Security
Technology
Tangled Dependencies
```
[^248]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.467)*

**Verbatim Educational Excerpt** *(Building Microservices, p.467, lines 14–21)*:
```
A Deployment Interface
Environment Definition
Summary
7. Testing
Types of Tests
Test Scope
Unit Tests
Service Tests
```
[^249]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.466)*

**Verbatim Educational Excerpt** *(Building Microservices, p.466, lines 19–26)*:
```
Build Pipelines and Continuous Delivery
And the Inevitable Exceptions
Platform-Specific Artifacts
Operating System Artifacts
Custom Images
Images as Artifacts
Immutable Servers
Environments
```
[^250]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.466)*

**Verbatim Educational Excerpt** *(Building Microservices, p.466, lines 19–26)*:
```
Build Pipelines and Continuous Delivery
And the Inevitable Exceptions
Platform-Specific Artifacts
Operating System Artifacts
Custom Images
Images as Artifacts
Immutable Servers
Environments
```
[^251]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.467)*

**Verbatim Educational Excerpt** *(Building Microservices, p.467, lines 8–15)*:
```
Two Case Studies on the Power of Automation
From Physical to Virtual
Traditional Virtualization
Vagrant
Linux Containers
Docker
A Deployment Interface
Environment Definition
```
[^252]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.468)*

**Verbatim Educational Excerpt** *(Building Microservices, p.468, lines 16–23)*:
```
Mean Time to Repair Over Mean Time Between Failures?
Cross-Functional Testing
Performance Tests
Summary
8. Monitoring
Single Service, Single Server
Single Service, Multiple Servers
Multiple Services, Multiple Servers
```
[^253]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Immutable** *(p.466)*

**Verbatim Educational Excerpt** *(Building Microservices, p.466, lines 24–26)*:
```
Images as Artifacts
Immutable Servers
Environments
```
[^254]
**Annotation:** This excerpt demonstrates 'immutable' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Logging** *(p.470)*

**Verbatim Educational Excerpt** *(Building Microservices, p.470, lines 3–10)*:
```
Firewalls
Logging
Intrusion Detection (and Prevention) System
Network Segregation
Operating System
A Worked Example
Be Frugal
The Human Element
```
[^255]
**Annotation:** This excerpt demonstrates 'logging' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Mock** *(p.467)*

**Verbatim Educational Excerpt** *(Building Microservices, p.467, lines 25–27)*:
```
Implementing Service Tests
Mocking or Stubbing
A Smarter Stub Service
```
[^256]
**Annotation:** This excerpt demonstrates 'mock' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Mutable** *(p.466)*

**Verbatim Educational Excerpt** *(Building Microservices, p.466, lines 24–26)*:
```
Images as Artifacts
Immutable Servers
Environments
```
[^257]
**Annotation:** This excerpt demonstrates 'mutable' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Open** *(p.469)*

**Verbatim Educational Excerpt** *(Building Microservices, p.469, lines 16–23)*:
```
HTTP(S) Basic Authentication
Use SAML or OpenID Connect
Client Certificates
HMAC Over HTTP
API Keys
The Deputy Problem
Securing Data at Rest
Go with the Well Known
```
[^258]
**Annotation:** This excerpt demonstrates 'open' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Pip** *(p.466)*

**Verbatim Educational Excerpt** *(Building Microservices, p.466, lines 18–25)*:
```
Mapping Continuous Integration to Microservices
Build Pipelines and Continuous Delivery
And the Inevitable Exceptions
Platform-Specific Artifacts
Operating System Artifacts
Custom Images
Images as Artifacts
Immutable Servers
```
[^259]
**Annotation:** This excerpt demonstrates 'pip' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Re** *(p.465)*

**Verbatim Educational Excerpt** *(Building Microservices, p.465, lines 1–8)*:
```
Integrating with Third-Party Software
Lack of Control
Customization
Integration Spaghetti
On Your Own Terms
The Strangler Pattern
Summary
5. Splitting the Monolith
```
[^260]
**Annotation:** This excerpt demonstrates 're' as it appears in the primary text. The concept occurs 12 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---

## Chapter 15: Organizational Structures

*Source: Building Microservices, 2nd Edition, pages 473–473*

### Chapter Summary
Discusses organizational structures and team topologies for microservices success. Covers Conway's Law implications, DevOps culture, service ownership models, team autonomy, cross-functional teams, governance approaches, organizational alignment, and fostering effective collaboration. [^261]

### Concept-by-Concept Breakdown
#### **Re** *(p.473)*

**Verbatim Educational Excerpt** *(Building Microservices, p.473, lines 1–8)*:
```
Dynamic Service Registries
Zookeeper
Consul
Eureka
Rolling Your Own
Don’t Forget the Humans!
Documenting Services
Swagger
```
[^262]
**Annotation:** This excerpt demonstrates 're' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Sys** *(p.473)*

**Verbatim Educational Excerpt** *(Building Microservices, p.473, lines 9–16)*:
```
HAL and the HAL Browser
The Self-Describing System
Summary
12. Bringing It All Together
Principles of Microservices
Model Around Business Concepts
Adopt a Culture of Automation
Hide Internal Implementation Details
```
[^263]
**Annotation:** This excerpt demonstrates 'sys' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---


---

### **Footnotes**

[^1]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 1, lines 1–25).
[^2]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 23, lines 7–14).
[^3]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 8, lines 6–11).
[^4]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 17, lines 7–14).
[^5]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 17, lines 1–8).
[^6]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 17, lines 4–11).
[^7]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 23, lines 15–16).
[^8]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 9, lines 19–26).
[^9]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 7, lines 9–14).
[^10]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 11, lines 3–10).
[^11]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 14, lines 17–21).
[^12]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 15, lines 2–9).
[^13]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 17, lines 4–11).
[^14]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 10, lines 11–18).
[^15]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 10, lines 26–28).
[^16]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 28, lines 4–11).
[^17]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 29, lines 1–1).
[^18]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 69, lines 1–1).
[^19]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 113, lines 1–1).
[^20]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 29, lines 1–25).
[^21]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 51, lines 4–11).
[^22]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 48, lines 8–15).
[^23]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 67, lines 3–10).
[^24]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 38, lines 2–9).
[^25]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 42, lines 2–9).
[^26]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 51, lines 6–13).
[^27]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 65, lines 5–12).
[^28]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 38, lines 3–10).
[^29]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 43, lines 2–9).
[^30]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 48, lines 8–15).
[^31]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 57, lines 1–8).
[^32]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 57, lines 1–8).
[^33]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 36, lines 2–9).
[^34]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 67, lines 12–19).
[^35]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 36, lines 3–10).
[^36]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 69, lines 1–1).
[^37]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 113, lines 1–1).
[^38]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 161, lines 1–1).
[^39]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 69, lines 1–25).
[^40]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 71, lines 8–15).
[^41]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 95, lines 10–17).
[^42]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 81, lines 1–5).
[^43]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 110, lines 1–8).
[^44]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 89, lines 1–8).
[^45]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 80, lines 4–7).
[^46]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 87, lines 15–22).
[^47]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 96, lines 29–36).
[^48]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 93, lines 3–10).
[^49]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 97, lines 6–12).
[^50]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 89, lines 26–33).
[^51]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 109, lines 7–8).
[^52]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 96, lines 8–15).
[^53]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 96, lines 8–15).
[^54]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 104, lines 14–21).
[^55]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 113, lines 1–1).
[^56]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 161, lines 1–1).
[^57]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 209, lines 1–1).
[^58]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 113, lines 1–25).
[^59]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 136, lines 8–15).
[^60]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 114, lines 10–17).
[^61]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 115, lines 2–9).
[^62]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 160, lines 1–8).
[^63]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 119, lines 1–8).
[^64]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 160, lines 2–9).
[^65]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 119, lines 1–8).
[^66]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 116, lines 10–17).
[^67]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 146, lines 20–21).
[^68]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 146, lines 20–21).
[^69]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 160, lines 13–20).
[^70]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 115, lines 35–38).
[^71]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 156, lines 2–9).
[^72]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 122, lines 5–12).
[^73]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 129, lines 12–18).
[^74]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 161, lines 1–1).
[^75]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 209, lines 1–1).
[^76]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 243, lines 1–1).
[^77]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 161, lines 1–25).
[^78]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 167, lines 2–9).
[^79]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 198, lines 14–21).
[^80]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 194, lines 2–9).
[^81]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 166, lines 1–8).
[^82]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 185, lines 23–29).
[^83]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 204, lines 6–13).
[^84]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 166, lines 14–18).
[^85]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 178, lines 6–11).
[^86]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 192, lines 7–14).
[^87]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 171, lines 10–17).
[^88]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 196, lines 1–8).
[^89]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 196, lines 1–8).
[^90]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 197, lines 2–9).
[^91]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 176, lines 7–14).
[^92]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 175, lines 1–8).
[^93]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 209, lines 1–1).
[^94]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 243, lines 1–1).
[^95]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 273, lines 1–1).
[^96]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 209, lines 1–25).
[^97]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 216, lines 14–21).
[^98]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 224, lines 7–14).
[^99]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 214, lines 1–8).
[^100]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 215, lines 6–13).
[^101]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 214, lines 9–16).
[^102]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 228, lines 1–8).
[^103]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 209, lines 3–10).
[^104]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 220, lines 4–11).
[^105]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 230, lines 16–21).
[^106]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 226, lines 3–10).
[^107]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 239, lines 2–9).
[^108]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 209, lines 21–28).
[^109]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 212, lines 10–17).
[^110]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 224, lines 14–21).
[^111]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 216, lines 3–10).
[^112]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 243, lines 1–1).
[^113]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 273, lines 1–1).
[^114]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 313, lines 1–1).
[^115]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 243, lines 1–25).
[^116]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 257, lines 1–8).
[^117]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 262, lines 1–8).
[^118]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 253, lines 3–10).
[^119]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 263, lines 2–9).
[^120]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 260, lines 20–27).
[^121]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 258, lines 16–23).
[^122]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 248, lines 11–18).
[^123]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 255, lines 6–13).
[^124]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 269, lines 14–20).
[^125]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 253, lines 9–16).
[^126]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 264, lines 1–8).
[^127]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 257, lines 5–12).
[^128]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 243, lines 13–20).
[^129]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 255, lines 7–14).
[^130]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 267, lines 1–8).
[^131]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 273, lines 1–1).
[^132]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 313, lines 1–1).
[^133]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 351, lines 1–1).
[^134]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 273, lines 1–25).
[^135]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 303, lines 13–15).
[^136]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 279, lines 1–8).
[^137]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 297, lines 1–8).
[^138]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 301, lines 9–16).
[^139]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 301, lines 9–16).
[^140]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 277, lines 14–21).
[^141]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 291, lines 3–10).
[^142]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 297, lines 31–37).
[^143]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 280, lines 13–18).
[^144]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 302, lines 3–10).
[^145]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 308, lines 1–4).
[^146]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 293, lines 5–12).
[^147]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 275, lines 25–32).
[^148]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 302, lines 5–11).
[^149]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 274, lines 21–28).
[^150]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 313, lines 1–1).
[^151]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 351, lines 1–1).
[^152]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 387, lines 1–1).
[^153]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 313, lines 1–25).
[^154]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 344, lines 5–12).
[^155]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 343, lines 1–8).
[^156]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 322, lines 21–26).
[^157]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 321, lines 4–11).
[^158]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 348, lines 21–28).
[^159]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 313, lines 14–21).
[^160]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 323, lines 17–19).
[^161]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 345, lines 12–19).
[^162]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 319, lines 3–10).
[^163]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 321, lines 10–11).
[^164]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 322, lines 8–15).
[^165]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 327, lines 10–15).
[^166]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 349, lines 1–8).
[^167]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 322, lines 8–15).
[^168]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 343, lines 12–19).
[^169]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 351, lines 1–1).
[^170]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 387, lines 1–1).
[^171]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 425, lines 1–1).
[^172]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 351, lines 1–25).
[^173]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 354, lines 1–8).
[^174]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 365, lines 9–12).
[^175]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 360, lines 1–8).
[^176]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 375, lines 1–8).
[^177]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 384, lines 11–18).
[^178]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 357, lines 1–8).
[^179]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 352, lines 8–15).
[^180]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 351, lines 19–26).
[^181]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 353, lines 20–27).
[^182]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 353, lines 31–38).
[^183]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 373, lines 5–11).
[^184]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 359, lines 1–8).
[^185]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 351, lines 1–8).
[^186]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 354, lines 26–33).
[^187]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 368, lines 3–10).
[^188]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 387, lines 1–1).
[^189]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 425, lines 1–1).
[^190]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 449, lines 1–1).
[^191]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 387, lines 1–25).
[^192]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 422, lines 8–15).
[^193]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 410, lines 3–10).
[^194]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 418, lines 7–14).
[^195]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 401, lines 2–9).
[^196]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 401, lines 1–8).
[^197]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 423, lines 10–17).
[^198]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 417, lines 2–9).
[^199]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 408, lines 12–19).
[^200]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 392, lines 1–8).
[^201]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 417, lines 13–17).
[^202]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 417, lines 13–17).
[^203]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 407, lines 5–12).
[^204]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 398, lines 17–24).
[^205]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 392, lines 7–14).
[^206]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 403, lines 2–9).
[^207]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 425, lines 1–1).
[^208]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 449, lines 1–1).
[^209]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 465, lines 1–1).
[^210]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 425, lines 1–25).
[^211]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 426, lines 10–17).
[^212]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 430, lines 1–8).
[^213]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 427, lines 2–9).
[^214]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 425, lines 1–8).
[^215]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 426, lines 15–22).
[^216]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 425, lines 3–10).
[^217]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 438, lines 20–24).
[^218]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 435, lines 2–9).
[^219]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 435, lines 2–9).
[^220]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 432, lines 6–13).
[^221]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 441, lines 16–23).
[^222]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 432, lines 2–9).
[^223]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 433, lines 6–13).
[^224]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 438, lines 20–24).
[^225]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 428, lines 5–12).
[^226]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 449, lines 1–1).
[^227]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 465, lines 1–1).
[^228]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 449, lines 1–25).
[^229]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 460, lines 3–10).
[^230]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 464, lines 5–12).
[^231]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 457, lines 7–14).
[^232]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 457, lines 9–16).
[^233]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 458, lines 6–11).
[^234]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 453, lines 14–21).
[^235]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 453, lines 14–21).
[^236]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 455, lines 8–15).
[^237]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 454, lines 21–23).
[^238]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 452, lines 2–9).
[^239]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 458, lines 6–11).
[^240]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 450, lines 6–13).
[^241]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 461, lines 24–26).
[^242]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 451, lines 4–11).
[^243]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 449, lines 1–8).
[^244]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 465, lines 1–1).
[^245]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 465, lines 1–25).
[^246]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 471, lines 15–22).
[^247]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 472, lines 1–8).
[^248]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 465, lines 9–16).
[^249]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 467, lines 14–21).
[^250]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 466, lines 19–26).
[^251]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 466, lines 19–26).
[^252]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 467, lines 8–15).
[^253]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 468, lines 16–23).
[^254]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 466, lines 24–26).
[^255]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 470, lines 3–10).
[^256]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 467, lines 25–27).
[^257]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 466, lines 24–26).
[^258]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 469, lines 16–23).
[^259]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 466, lines 18–25).
[^260]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 465, lines 1–8).
[^261]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 473, lines 1–25).
[^262]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 473, lines 1–8).
[^263]: Newman, Sam. *Building Microservices, 2nd Edition*. (JSON `Building Microservices.json`, p. 473, lines 9–16).
