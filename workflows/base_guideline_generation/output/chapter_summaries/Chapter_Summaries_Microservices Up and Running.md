# Comprehensive Python Guidelines — Microservices Up and Running (Chapters 1-12)

*Source: Microservices Up and Running, Chapters 1-12*

---

## Chapter 1: Microservices: The What and the Why

*Source: Microservices Up and Running, pages 1–20*

### Chapter Summary
Introduces microservices architecture, defining what microservices are and explaining why organizations adopt them. Covers key characteristics, principles, the shift from monolithic to distributed systems, service modularity, independence, and the fundamental concepts of bounded contexts and service autonomy. [^1]

### Concept-by-Concept Breakdown
#### **Gil** *(p.18)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.18, lines 1–8)*:
```
safer change means more agility for your business. That agility translates to better
outcomes for your business and your organization.
The trick to unlocking all that value is to have the right architecture in place to sup‐
port the services. It needs to reduce system costs, without diminishing the value of
independent services. To build that architecture, you’ll need to make important deci‐
sions early. Those decisions will span methods, processes, teams, technologies, and
tools. They’ll also need to work together to form an emergent, optimized whole.
A good way to build a system like this is through evolution. You could start with a few
```
[^2]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.20)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.20, lines 2–9)*:
```
Companies around the world have had success implementing microservices architec‐
tures. Almost universally, the practitioners we’ve talked to have reported an increase
in speed of software delivery. We believe that improvement comes from the funda‐
mental benefit of the microservices style: a reduction in coordination costs.
It should be pointed out that there are many ways to increase speed in software engi‐
neering. Building software the microservices way is just one option. For example, you
could build a system quickly by cutting corners and incurring “technical debt” that
you’ll deal with later. Or, you could focus less on stability and safety and just get your
```
[^3]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 12 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.8)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.8, lines 22–29)*:
```
Context Mapping                                                                                                          62
Synchronous Versus Asynchronous Integrations                                                   65
A DDD Aggregate                                                                                                        66
Introduction to Event Storming                                                                                    66
The Event-Storming Process                                                                                      68
Introducing the Universal Sizing Formula                                                                   73
The Universal Sizing Formula                                                                                    74
Summary                                                                                                                           74
```
[^4]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.18)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.18, lines 30–37)*:
```
microservices possess. Their list starts with the core microservice characteristic of
componentization via services, which means breaking an application into smaller serv‐
ices. From there they go on to cover a wide breadth of capabilities. They document
the need for organizational and management design with the characteristics of orga‐
nization around business capabilities and decentralized governance. They hint at
DevOps and Agile delivery practices when they introduce infrastructure automation
and products not projects. They also identify a few key architecture principles, such as
smart endpoints and dumb pipes, design for failure, and evolutionary design.
```
[^5]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.13)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.13, lines 3–10)*:
```
microservices to define a style of software architecture that had evolved. Since that
time, there’s been an explosion of classes, videos, and written works for the microser‐
vices style. In fact, in 2016 we coauthored Microservice Architecture, a book that
offered an introductory guide to the principles of a microservices system.
Since the publication of that book, we and many others have had a chance to live with
the microservices systems we’ve built. Our own experiences, as well as conversations
with other practitioners, have led to a better understanding of the practical problems
that implementers face. A lot of that understanding comes from success, but some of
```
[^6]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.13)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.13, lines 23–28)*:
```
building microservices or a microservices architecture, this is the book for you.
But this book is also a useful guide for readers who simply want to get “up close and
personal” with a microservices implementation. No matter what your role is, if you’re
interested in understanding the work that goes into building a microservices system,
you’ll find this book enlightening.
xi
```
[^7]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.19)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.19, lines 4–11)*:
```
ing, operationalization, governance, team structure, and culture.
For contrast, here is another definition for microservices from the book Microservice
Architecture by Irakli Nadareishvili, Ronnie Mitra, Matt McLarty, and Mike Amund‐
sen (O’Reilly):
A microservice is an independently deployable component of bounded scope that sup‐
ports interoperability through message-based communication. Microservice architec‐
ture is a style of engineering highly automated, evolvable software systems made up of
capability-aligned microservices.
```
[^8]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.14)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.14, lines 19–26)*:
```
Italic
Indicates new terms, URLs, email addresses, filenames, and file extensions.
Constant width
Used for program listings, as well as within paragraphs to refer to program ele‐
ments such as variable or function names, databases, data types, environment
variables, statements, and keywords.
Constant width bold
Shows commands or other text that should be typed literally by the user.
```
[^9]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.16)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.16, lines 30–35)*:
```
David Butland for the incredible insight, feedback, and observations they provided.
Finally, we’d like to thank Capital One and Publicis Sapient for the support they pro‐
vided in allowing us to bring this book to life.
xiv 
| 
Preface
```
[^10]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.15)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.15, lines 11–18)*:
```
need to contact us for permission unless you’re reproducing a significant portion of
the code. For example, writing a program that uses several chunks of code from this
book does not require permission. Selling or distributing examples from O’Reilly
books does require permission. Answering a question by citing this book and quoting
example code does not require permission. Incorporating a significant amount of
example code from this book into your product’s documentation does require
permission.
We appreciate, but generally do not require, attribution. An attribution usually
```
[^11]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.14)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.14, lines 22–29)*:
```
Used for program listings, as well as within paragraphs to refer to program ele‐
ments such as variable or function names, databases, data types, environment
variables, statements, and keywords.
Constant width bold
Shows commands or other text that should be typed literally by the user.
Constant width italic
Shows text that should be replaced with user-supplied values or by values deter‐
mined by context.
```
[^12]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Global** *(p.5)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.5, lines 4–8)*:
```
To Lucas, who was born shortly after we started working on this book and whose smiles
gave me the strength to complete this book in the middle of a global pandemic; to my
wife Ana, for her support; and to my amazing students at Temple University, in Phila‐
delphia, who kindly “test drove” early versions of a lot of the content in this book.
—Irakli
```
[^13]
**Annotation:** This excerpt demonstrates 'global' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Immutable** *(p.9)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.9, lines 8–15)*:
```
DevOps Principles and Practices                                                                                   98
Immutable Infrastructure                                                                                           99
Infrastructure as Code                                                                                               100
Continuous Integration and Continuous Delivery                                               102
Setting Up the IaC Environment                                                                                 104
Set Up GitHub                                                                                                            104
Install Terraform                                                                                                        105
Configuring Amazon Web Services                                                                            106
```
[^14]
**Annotation:** This excerpt demonstrates 'immutable' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.18)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.18, lines 4–11)*:
```
port the services. It needs to reduce system costs, without diminishing the value of
independent services. To build that architecture, you’ll need to make important deci‐
sions early. Those decisions will span methods, processes, teams, technologies, and
tools. They’ll also need to work together to form an emergent, optimized whole.
A good way to build a system like this is through evolution. You could start with a few
small decisions and learn and grow as you go. In fact, most early adopters ended up
with microservices through iterative experimentation. They didn’t set out with a goal
of building a microservices-based application. Instead, they ended up with them
```
[^15]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **List** *(p.19)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.19, lines 1–8)*:
```
Each of these characteristics is worth understanding, and we encourage you to read
their article if you haven’t already. Together, these characteristics form a holistic solu‐
tion with a very large set of concerns. It includes technology, infrastructure, engineer‐
ing, operationalization, governance, team structure, and culture.
For contrast, here is another definition for microservices from the book Microservice
Architecture by Irakli Nadareishvili, Ronnie Mitra, Matt McLarty, and Mike Amund‐
sen (O’Reilly):
A microservice is an independently deployable component of bounded scope that sup‐
```
[^16]
**Annotation:** This excerpt demonstrates 'list' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 2: The Microservices Value Proposition** *(pp.21–38)*

This later chapter builds upon the concepts introduced here, particularly: GIL, as, close.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^17]

**Annotation:** Forward reference: Chapter 2 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 3: Designing Microservices Systems** *(pp.39–64)*

This later chapter builds upon the concepts introduced here, particularly: GIL, as, class.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^18]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Establishing a Foundation** *(pp.65–96)*

This later chapter builds upon the concepts introduced here, particularly: GIL, as, async.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^19]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 2: The Microservices Value Proposition

*Source: Microservices Up and Running, pages 21–38*

### Chapter Summary
Explores the business value proposition of microservices including organizational agility, scalability benefits, resilience, technology flexibility, and innovation enablement. Discusses time to market improvements, team autonomy, competitive advantages, and the return on investment from microservices adoption. [^20]

### Concept-by-Concept Breakdown
#### **Gil** *(p.22)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.22, lines 1–8)*:
```
makes a lot of sense. The microservices style enables companies operating in complex
domains to have the agility of a simpler, smaller company while continuing to harness
the power and reach of their actual size. It’s incredibly appealing and the growth in
adoption proves that—however, the benefits don’t come for free. It takes a lot of up-
front work, focus, and decision making to build a microservices architecture that can
unlock that value.
The Hard Parts
One of the biggest hurdles that first-time microservices adopters face is dealing with
```
[^21]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.23)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.23, lines 2–9)*:
```
When we compound the problem of long feedback loops for our decision with
the complex system we need to design, it’s easy to see why microservices architec‐
ture is a challenge. The decisions you need to make are both highly impactful and
difficult to measure. This can lead to endless speculation, discussion, and evalua‐
tion of architectural decisions because of the fear of making the wrong kind of
system. Instead of building a system that can achieve business outcomes, we end
up in a state of indecision, trying to model the endless permutations of our
choices. This condition is commonly known as analysis paralysis. It doesn’t help
```
[^22]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 15 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.32)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.32, lines 27–34)*:
```
structure is a copy of the organization’s communication structure.
—Attributed to Fred Brooks
Conway tells us that the output of an organization reflects the way its people and
teams communicate. For example, consider a microservices team that must consult a
centralized team of database experts whenever they need to change a data model.
Chances are that the data model and data implementation will also be centralized in
the system that gets produced. The system ends up matching the organization and
coordination model.
```
[^23]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.33)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.33, lines 1–8)*:
```
people factors that have the biggest impact on a microservices system: team size, team
skills, and interteam coordination. Let’s take a closer look at each of them, starting
with size.
Team Size
The “micro” in microservices implies that size matters and smaller is best. To be hon‐
est, that’s a bit of an oversimplification. But the truth remains: buliding smaller
deployable services is an important part of succeeding with microservices. It also
turns out that the size of the teams building those services matters a lot too.
```
[^24]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.23)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.23, lines 28–35)*:
```
methodology, and build microservices of various sizes. As long as you could measure
your results, you’d continue to improve the system. With enough trials, you’d end up
with a system that works for you as well as a lot of experience building microservice
systems.
Chances are, though, that you don’t have the luxury of unlimited time. So, how do
you build the expertise you need to build better microservices?
To help address this challenge, we’ve developed a prescriptive microservices model.
We’ve made decisions about team design, process, architecture, infrastructure, and
```
[^25]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.31)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.31, lines 11–18)*:
```
tem. It shapes all the decision making and work that you do when you build software.
For example, an operating model can define the responsibilities of teams. It can also
define governance over decision making and work.
You can think of the operating model as the “operating system” for your solution. All
the work needed to build microservices happens on top of the team structures, pro‐
cesses, and boundaries you define. In practice, operating models can have a big scope
and can be very detailed. But for our build, we’ll reduce the scope and focus on the
most important parts of a microservices system—how the teams are designed and
```
[^26]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.27)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.27, lines 4–11)*:
```
we work or other decisions that need to be made?
You can create decision records however you like. You can write them up as text files,
use a project management tool, or even track them in a spreadsheet. The format and
tooling is less important than the content. As long as you capture the areas we’ve
described you’ll have a good decision record.
For our example project, we’ll use an existing format called a lightweight architectural
decision record (LADR). The LADR format was created by Michael Nygard, and is a
nice concise way of documenting a decision record. Let’s get to know LADR by build‐
```
[^27]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.25)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.25, lines 29–36)*:
```
developed. To do this, we’ll use a set of technologies including DockerHub,
Kubernetes, Helm, and Argo CD. Finally, after release, we’ll take a retrospective
look at the system in Chapter 11.
The model we’ve developed is built on a set of five guiding princi‐
ples, including the twelve-factor app pattern. If you’re interested,
you can read about our model’s guiding principles at this book’s
GitHub repository.
Learning by Doing 
```
[^28]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.32)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.32, lines 4–11)*:
```
The model we’re using in this book is mostly concerned with technology and tool
decisions. But technology alone won’t give you the value you need from a microservi‐
ces system. Technology is important. Good technology choices make it easier for you
to do things that may have been prohibitively difficult. At its best, technology opens
doors and unlocks new opportunities. However, it’s useless on its own.
You can have the world’s best tools and platforms, but you’ll fail if you don’t have the
right culture and organization in which to use them. The goal we’re trying to reach in
our model is to put good technology in the hands of independent, high-functioning
```
[^29]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.34)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.34, lines 28–35)*:
```
there is a general principle we can adopt that seems to help microservices implement‐
ers universally. That’s the principle of the cross-functional team.
In a cross-functional team, people with different types of expertise (or functions)
work together toward the same goal. That expertise can span both technology and
business domains. For example, a cross-functional team could contain UX designers,
application developers, product owners, and business analysts.
18 
| 
```
[^30]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.32)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.32, lines 1–8)*:
```
Let’s get started by taking a look at why teams and team design are so important in
the first place.
Why Teams and People Matter
The model we’re using in this book is mostly concerned with technology and tool
decisions. But technology alone won’t give you the value you need from a microservi‐
ces system. Technology is important. Good technology choices make it easier for you
to do things that may have been prohibitively difficult. At its best, technology opens
doors and unlocks new opportunities. However, it’s useless on its own.
```
[^31]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Iteration** *(p.23)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.23, lines 22–29)*:
```
decisions. Many of the successful microservices implementers we’ve talked to have
built their systems through continual iteration and improvement. Frequently, they’ve
had to build architectures that failed before they unlocked an understanding of how
to build a system that works.
If you had unlimited time, you could build a great microservices architecture solely
through experimentation. You could adopt endless organizational models, try every
methodology, and build microservices of various sizes. As long as you could measure
your results, you’d continue to improve the system. With enough trials, you’d end up
```
[^32]
**Annotation:** This excerpt demonstrates 'iteration' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **List** *(p.27)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.27, lines 13–20)*:
```
If you want to use something other than LADR, Joel Parker Hen‐
derson maintains a great list of ADR formats and templates.
Writing a Lightweight Architectural Decision Record
The first key decision we’ll record is the decision to keep a record of decisions. Put
more simply, we’ll create an ADR that says we intend to keep track of our decisions.
As we’ve mentioned, we’ll be using the LADR format. The nice thing about LADR is
that it’s designed to be lightweight. It lets us keep track of decisions in simple text files
that we can write quickly. Since we’re dealing with text files, we can even manage our
```
[^33]
**Annotation:** This excerpt demonstrates 'list' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Method** *(p.36)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.36, lines 5–12)*:
```
and deployment decisions, there would be no “organizational friction” to slow things
down. In our experience this isn’t a practical method of operation.
That’s because coordination and collaboration are important for the success of an
organization. We might want our microservices teams to act independently, but we
also want them to create services that are valuable to customers, users, and the orga‐
nization. This means communication is required to establish shared goals, communi‐
cate change requests, deliver feedback, and resolve problems.
On top of this, when teams operate completely independently, there’s less opportunity
```
[^34]
**Annotation:** This excerpt demonstrates 'method' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Open** *(p.27)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.27, lines 26–31)*:
```
down and present it as a formatted, human-readable document.
To create our first Markdown-based LADR, open your favorite text editor and start
working on a new document. The first thing we’ll do is lay out the structure.
Decisions, Decisions… 
| 
11
```
[^35]
**Annotation:** This excerpt demonstrates 'open' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 3: Designing Microservices Systems** *(pp.39–64)*

This later chapter builds upon the concepts introduced here, particularly: GIL, as, close.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^36]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Establishing a Foundation** *(pp.65–96)*

This later chapter builds upon the concepts introduced here, particularly: GIL, as, attribute.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^37]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Service Design** *(pp.97–134)*

This later chapter builds upon the concepts introduced here, particularly: as, close, def.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^38]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, close appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 3: Designing Microservices Systems

*Source: Microservices Up and Running, pages 39–64*

### Chapter Summary
Details designing microservices systems using domain-driven design principles. Covers service decomposition strategies, defining bounded contexts and service boundaries, aligning services with business capabilities, API design, managing coupling and cohesion, and creating modular architectures with clear interface contracts. [^39]

### Concept-by-Concept Breakdown
#### **Gil** *(p.57)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.57, lines 25–32)*:
```
actual actor for the Job Story is.
If you are familiar with User Stories from Scrum or other Agile methodologies, you
may have noticed that the Job Story looks almost identical. However, as Alan Klement
explains in his blog post, “Replacing the User Story with the Job Story”, there are cru‐
cial differences between the two. User Stories revolve around a user persona; they
Identifying Jobs That Actors Have to Do 
| 
41
```
[^40]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.60)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.60, lines 9–16)*:
```
• Easily and effectively version-control sources of the diagrams. Text files are easy
to diff, merge, and review in pull requests, none of which would be true for a
binary graphic file.
• Conveniently integrate modeling into the release process. The diagrams become
code and anything you can do with the code, you can now do with your diagrams
as well; if you also version-control them in a system like Git, for example.
Key Decision: Use PlantUML Sequence Diagrams
to Discover Interaction Patterns
```
[^41]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.53)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.53, lines 35–42)*:
```
scoping and prioritization. Typical plagues of API and service design in our industry
are overabstraction and lack of clarity regarding user needs. Too many APIs are sim‐
ply exposures of some database tables over HTTP or an attempt to provide direct net‐
worked access into application internals, via remote procedure calls (RPCs). Such
approaches often struggle in delivering for customer needs and achieving business
Identifying Actors 
| 
37
```
[^42]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.53)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.53, lines 1–8)*:
```
Let’s explore each of these steps in greater detail and see how we can master using
them for service design.
Identifying Actors
In addition to being an evolutionary methodology, SEED(S) takes a distinctly
customer-centric approach, viewing as products the services it is used to design. By
now the “APIs are products” mantra is not particularly novel; we have been shouting
it from all possible mountaintops for years. The good thing is that a product-oriented
perspective on APIs and services allows us to reuse a wealth of techniques from the
```
[^43]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 19 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.43)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.43, lines 9–16)*:
```
microservices teams later on when we need them. Or, if you have a programming
background, you can think of this as defining a “class,” for which we’ll be creating
“instances” later.
To get started, we’ll do the same thing we did for our system design team—define
some essential team properties. Just like before, we’ll document the team type, team
size, and responsibilities. As we mentioned before, our microservices teams are
expected to own one or more microservices independently. That ownership includes
running the service and releasing a continuous stream of improvements, fixes, and
```
[^44]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.39)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.39, lines 9–16)*:
```
Collaboration
This interaction mode requires both teams to work closely together. Collabora‐
tion provides opportunities for teams to learn, discover, and innovate. But it
requires high levels of coordination from each team and is difficult to scale. For
example, a security team might collaborate with a microservices team to develop
a more secure version of their software. The collaborative work might entail
designing, writing, and testing code together.
Facilitating
```
[^45]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.61)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.61, lines 19–24)*:
```
design process. Following Bertrand Meyer’s command query separation (CQS) prin‐
ciple,2 in SEED(S) we model a system’s interface contracts as collections of two dis‐
tinct types of interactions: the actions (“commands” in CQS) and the queries.
Deriving Actions and Queries from JTBDs 
| 
45
```
[^46]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.56)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.56, lines 2–9)*:
```
School, 2016, https://oreil.ly/NKolz.
Well, what is a general definition of a product, anyway? There is no one, true defini‐
tion that we are aware of, so we might as well use the one Wikipedia references:
We define a product as anything that can be offered to a market for attention, acquisi‐
tion, use or consumption that might satisfy a want or need. Products include more
than just tangible objects, such as cars, computers or mobile phones. Broadly defined,
“products” also include services, events, persons, places, organizations and ideas, or
mixes of these.
```
[^47]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Development Speed** *(p.51)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.51, lines 4–11)*:
```
If you recall, in Chapter 1, we stated that the main benefit of adopting microservices
architecture is the ability to increase development speed without compromising
safety of a system, at scale. This is an extremely important benefit for organizations
tackling significantly complex problems. Note though that this certainly happens as a
result of a conscious design, not by accident. In all but the simplest cases, it is impos‐
sible to iterate toward a successful microservices architecture without an effective and
explicit, end-to-end system design.
In this chapter, we introduce an evolutionary process for designing microservices.
```
[^48]
**Annotation:** This excerpt demonstrates 'development speed' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.56)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.56, lines 30–37)*:
```
alternative solution to getting quarter-inch holes in customer walls. It may be a chem‐
ical reaction of sorts or something else—we wouldn’t know—but it will happen.
If you look at the history of technological advancement, it’s the problems that are
timeless; solutions change and evolve all the time. Case in point—nobody uses mag‐
netic tapes or floppy disks to save data anymore, but the job of needing to save and
transport data has not gone anywhere, even if it is all cloud-based now. Innovators
must concentrate more on solving problems, and less on perfecting the tools that are
typically transient.
```
[^49]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.42)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.42, lines 2–9)*:
```
document for the system design team. Using your favorite text or document editor,
create a file named system-design-team.md and populate it with the following content:
# System Design Team
## Team Type
Enabling
## Team Size
3-5 People
## Responsibilities
```
[^50]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.41)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.41, lines 16–23)*:
```
Continually improve the system
Finally, the system design team needs to continually improve all the team
designs, standards, incentives, and guardrails that have been introduced. To do
that, they’ll need to establish a way of monitoring or measuring the system as a
whole so that they can make changes and introduce improvements.
It’s useful to document these team responsibilities so that we can clearly communicate
what each team does. In fact, we should document all of the key properties of our
teams to make it easier to understand and improve them as the system evolves. At a
```
[^51]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.56)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.56, lines 1–8)*:
```
1 Quoted in Clayton M. Christensen et al., “What Customers Want from Your Products,” Harvard Business
School, 2016, https://oreil.ly/NKolz.
Well, what is a general definition of a product, anyway? There is no one, true defini‐
tion that we are aware of, so we might as well use the one Wikipedia references:
We define a product as anything that can be offered to a market for attention, acquisi‐
tion, use or consumption that might satisfy a want or need. Products include more
than just tangible objects, such as cars, computers or mobile phones. Broadly defined,
“products” also include services, events, persons, places, organizations and ideas, or
```
[^52]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.49)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.49, lines 11–18)*:
```
and consumer demands. A special nuance of the API team is that, because the API
needs to call microservices to function, it is dependent on the microservices team.
We can model these interaction properties in our Team Topology model by adding
another rectangle at the top of our diagram to represent the API team. It should be of
the same color as the microservices team (we’ve used yellow), as it is also a stream-
aligned team. To reflect the dependency between our microservices and API teams,
we’ll again use a black arrow to show an x-as-a-service engagement model. This indi‐
cates that the microservices team will need to make sure their services are invocable
```
[^53]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.42)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.42, lines 30–36)*:
```
ing a microservice. In practice, a single team may own multiple microservices. This is
fine, and avoids unnecessary growth of teams. The most important constraint is that
the responsibility for a microservice is not shared across multiple teams. Microser‐
vice ownership will be limited to an accountable and responsible team.
26 
| 
Chapter 2: Designing a Microservices Operating Model
```
[^54]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 4: Establishing a Foundation** *(pp.65–96)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^55]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Service Design** *(pp.97–134)*

This later chapter builds upon the concepts introduced here, particularly: None, as, class.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^56]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Service Communication** *(pp.135–178)*

This later chapter builds upon the concepts introduced here, particularly: as, class, def.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^57]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, class appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 4: Establishing a Foundation

*Source: Microservices Up and Running, pages 65–96*

### Chapter Summary
Focuses on establishing the foundational platform and infrastructure for microservices. Covers infrastructure automation, CI/CD pipelines, containerization, Kubernetes orchestration, cloud platforms, service mesh technology, observability foundations, monitoring, logging, and essential tooling for microservices ecosystems. [^58]

### Concept-by-Concept Breakdown
#### **Gil** *(p.92)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.92, lines 14–21)*:
```
The process of releasing code through a deployment pipeline becomes significantly
more complex and fragile if a deployment of one microservice triggers ripple effects
of having to also redeploy other parts of the application. Such interdependencies can
compromise both the speed and safety of the entire system. Alternatively, if we can
ensure that we can always deploy each microservice independently, without having to
worry about the ripple effects, we can keep our deployments nimble and safe.
There can be a number of reasons why you may not be able to make a deployment of
your microservices independent, but in the context of data management, the most
```
[^59]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.81)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.81, lines 19–26)*:
```
Integration interfaces between bounded contexts can be synchronous or asynchro‐
nous, as shown in Figure 4-8. None of the integration patterns fundamentally assume
one or the other style.
Common patterns for synchronous integrations between contexts are RESTful APIs
deployed over HTTP, gRPC services using binary formats such as protobuf, and more
recently services using GraphQL interfaces.
On the asynchronous side, publish–subscribe types of interactions lead the way. In
this interaction pattern, the Upstream can generate events, and Downstream services
```
[^60]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.66)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.66, lines 33–40)*:
```
                    seats:
                      type: array
                      items:
                        type: string
                returning:
                  type: object
                  properties:
                    flight_num:
```
[^61]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.94)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.94, lines 4–11)*:
```
Embedding Data Should Not Lead to an Explosion in the Number of
Database Clusters
When building complex applications, we can often end up with different kinds of
databases. Datasets in those databases (e.g., “tables” for relational databases) should
never have multiple microservices as co-owners. When you build big systems, you
could eventually have hundreds of microservices. Does it then mean that we have to
deploy hundreds of distinct clusters of Cassandra, Postgres, Redis, or MySQL? Teams
implementing microservices need clarity on how far they should take the notion of
```
[^62]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 25 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.76)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.76, lines 38–42)*:
```
the Heart of Software (Addison-Wesley). The main premise of the methodology is the
assertion that, when analyzing complex systems, we should avoid seeking a single
60 
| 
Chapter 4: Rightsizing Your Microservices: Finding Service Boundaries
```
[^63]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.76)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.76, lines 38–42)*:
```
the Heart of Software (Addison-Wesley). The main premise of the methodology is the
assertion that, when analyzing complex systems, we should avoid seeking a single
60 
| 
Chapter 4: Rightsizing Your Microservices: Finding Service Boundaries
```
[^64]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.81)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.81, lines 17–24)*:
```
ate based on the integration types used between bounded contexts.
Synchronous Versus Asynchronous Integrations
Integration interfaces between bounded contexts can be synchronous or asynchro‐
nous, as shown in Figure 4-8. None of the integration patterns fundamentally assume
one or the other style.
Common patterns for synchronous integrations between contexts are RESTful APIs
deployed over HTTP, gRPC services using binary formats such as protobuf, and more
recently services using GraphQL interfaces.
```
[^65]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.77)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.77, lines 28–34)*:
```
tials used for authentication and authorization. For a customer management-
bounded context, an account is a set of demographic and contact attributes, while for
a financial accounting context, it’s probably payment information and a list of past
transactions. We can see that the same basic English word is used with significantly
Domain-Driven Design and Microservice Boundaries 
| 
61
```
[^66]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.80)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.80, lines 7–14)*:
```
patibility. When Upstream modifies their service, they need to ensure that they
do not break anything for the customer. More dramatically, the Downstream
(customer) carries the risk of the Upstream intentionally or unintentionally
breaking something for it, or ignoring the customer’s future needs.
Conformist
An extreme case of the risks for a customer–supplier relationship is the conform‐
ist relationship. It’s a variation on Upstream–Downstream, when the Upstream
explicitly does not or cannot care about the needs of its Downstream. It’s a use-
```
[^67]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.77)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.77, lines 20–27)*:
```
importance of this observation lies in acknowledging that same words may carry dif‐
ferent meanings in different bounded contexts. A classic example of this is shown in
Figure 4-1. The term account carries significantly different meaning in the identity
and access management, customer management, and financial accounting contexts of
an online reservation system.
Figure 4-1. Depending on the domain where it appears, “account” can have different
meanings
Indeed, for an identity and access management context, an account is a set of creden‐
```
[^68]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.73)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.73, lines 16–23)*:
```
modeling, and decomposition of large domains (Domain-Driven Design), explain the
efficiency benefits of using Event Storming for domain analysis, and close by intro‐
ducing the Universal Sizing Formula, a unique guidance for the effective sizing of
microservices.
Why Boundaries Matter, When They Matter, and How to
Find Them
Right in the title of the architectural pattern, we have the word micro—the architec‐
ture we are designing is that of “micro” services! But how “micro” should our services
```
[^69]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.77)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.77, lines 7–14)*:
```
bounded context. Specifically, he stated that:
A Bounded Context defines the range of applicability of each model.
Bounded contexts allow implementation and runtime execution of different parts of
the larger system to occur without corrupting the independent domain models
present in that system. After defining bounded contexts, Eric went on to also help‐
fully provide a formula for identifying the optimal edges of a bounded context by
establishing the concept of Ubiquitous Language.
To understand the meaning of Ubiquitous Language, it is important to observe that a
```
[^70]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Descriptor** *(p.65)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.65, lines 16–23)*:
```
to work well is the VS Code editor with the Open API Designer plug-in. Once you
have the plug-in installed and a descriptor YAML file open inside the active tab, press
CTRL+ALT+P on Windows or CMD+ALT+P on macOS and choose the appropriate
preview command to see the rendering of the specification, as shown in Figure 3-3.
Figure 3-3. Selecting OAS Preview in VS Code
Example OAS for an Action in Our Sample Project
A simple version of the OAS for the rebooking action we described earlier in this
chapter may look something like the following:
```
[^71]
**Annotation:** This excerpt demonstrates 'descriptor' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.76)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.76, lines 10–17)*:
```
Features present in a service should be highly related, while unrelated features
should be encapsulated elsewhere. This way, if you need to change a logical unit
of functionality, you should be able to change it in one place, minimizing time to
releasing that change (an important metric). In contrast, if we had to change the
code in a number of services, we would have to release lots of different services at
the same time to deliver that change. That would require significant levels of
coordination, especially if those services are “owned” by multiple teams, and it
would directly compromise our goal of minimizing coordination costs.
```
[^72]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Encapsulation** *(p.74)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.74, lines 27–34)*:
```
bilities,” not technical needs. Similarly, Parnas, in an article from 1972, recom‐
mends decomposing systems based on modular encapsulation of design changes
over time. Neither approach necessarily aligns strongly with the boundaries of
serverless functions.
Too much granularity, too soon
An explosive level of granularity early in the microservices project life cycle can
introduce crushing levels of complexity that will stop the microservices effort in
its tracks, even before it has a chance to take off and succeed.
```
[^73]
**Annotation:** This excerpt demonstrates 'encapsulation' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 5: Service Design** *(pp.97–134)*

This later chapter builds upon the concepts introduced here, particularly: None, as, class.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^74]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Service Communication** *(pp.135–178)*

This later chapter builds upon the concepts introduced here, particularly: as, attribute, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^75]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, attribute appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Working with Data** *(pp.179–208)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^76]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 5: Service Design

*Source: Microservices Up and Running, pages 97–134*

### Chapter Summary
Examines service design patterns and best practices including API design principles, interface contracts, versioning strategies, and backwards compatibility. Covers REST APIs, gRPC, GraphQL, asynchronous messaging patterns, event-driven design, idempotency, and stateless service design. [^77]

### Concept-by-Concept Breakdown
#### **None** *(p.98)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.98, lines 10–17)*:
```
reservations, and notifications, to be specific. Most importantly, we would typically
want all three steps to happen or none of them to happen. For instance, let’s say we
suddenly find out that the requested seat is no longer available. Perhaps when we
started the process of deducting the miles for the payment, the seat was available, but
by the time we finished the process, somebody had already reserved that seat. Obvi‐
ously we can’t reserve this seat twice, so we must consider what to do in that situation.
In a busy-enough system, such race conditions and failures are inevitable, so when
they do occur, we need to roll back the entire process. We clearly need to refund the
```
[^78]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.116)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.116, lines 1–8)*:
```
This lends itself very well to the model we’re targeting. So, let’s make that our first key
decision for our infrastructure foundation.
Key Decision: Apply the Principle of Immutable Infrastructure
Infrastructure components must not be changed after they’ve been created. Changes
must be made by re-creating the component (and any dependent components) with
the new or altered properties.
The decision we’ve just made comes with a trade-off: the cost of destroying and re-
creating configurations. So we’ll need to make some additional decisions to make this
```
[^79]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 23 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.102)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.102, lines 8–15)*:
```
any experience with Event Sourcing. That said, we can easily find examples of Event-
Sourcing systems in real life. If you’ve ever seen an accounting journal, it is a classic
event store. Accountants record individual transactions, and the balance is a result of
summing up all transactions. Accountants are not allowed to record “state”; i.e., they
just write down the resulting balance after each transaction, without capturing the
transactions themselves. Similarly, if you have played chess and have recorded a chess
game, you would not write down the position of each piece on the board after each
move. Instead you are recording moves individually, and after each move the state of
```
[^80]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.107)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.107, lines 23–30)*:
```
for the banking application example earlier, it made a lot of sense because this
approach closely aligns with what happens in real life anyway. Banks calculate various
types of balances at the end of the month, quarter, and year; this is known as “closing
the books.” You should always try to find natural time points in your own domains
and align your snapshots with them.
Later in this chapter we will see that with a pattern called Command Query Responsi‐
bility Segregation (CQRS), we can do much more than just cache states in rolling
snapshots.
```
[^81]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.117)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.117, lines 1–8)*:
```
IaC is also very important for enabling our immutable infrastructure. Immutability
requires us to manage definitions for objects so they can be changed through re-
creation. There are plenty of ways to do that, but IaC lets us treat infrastructure the
way we treat applications. With IaC, creating and changing components is similar to
running a program. We’ll get to apply our know-how from the application develop‐
ment world to the infrastructure.
IaC is a good fit for the system we’re trying to build, so let’s formalize this decision
with an ADR.
```
[^82]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.101)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.101, lines 4–11)*:
```
next section we will discuss a powerful duo of design patterns: Event Sourcing and
CQRS. These can pretty much address everything else remaining, providing a com‐
plete toolset for data management in a microservices environment.
Event Sourcing and CQRS
Up to this point we have discussed some ways to avoid data sharing when using tradi‐
tional, relational data modeling. We showed how you can solve some of the data-
sharing challenges, but eventually, for advanced scenarios, we will run into cases
where relational modeling itself falls short of allowing the desired levels of data isola‐
```
[^83]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.104)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.104, lines 17–24)*:
```
Along the way several preferences were also added and updated, bringing the system
to the same state as in Figure 5-7, except here we can see the exact sequence of “facts”
that led to the current state, as opposed to just looking at the result in the state-
oriented representation.
So the sequence of events on the diagram gives you the same state that we had in the
relational data model. It is equivalent to what we had there, except this looks very,
very different. For instance, you may notice it looks much more uniform. There are
significantly fewer opinionated decisions to be made about the various entity types
```
[^84]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.131)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.131, lines 6–13)*:
```
the environment looks like and the last operations it’s performed. Terraform keeps
track of all that information in a JSON-based state file that is read and updated every
time it is run.
By default, Terraform will keep this state file in your local filesystem. In practice, stor‐
ing the state file locally is problematic. State often needs to be shared across machines
and users so that an environment can be managed in multiple places. However, local
state files are difficult to share and you can easily find yourself dealing with state con‐
flicts and synchronization issues.
```
[^85]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.112)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.112, lines 4–10)*:
```
oper workspace—a critical foundation for creating an enjoyable developer experience
in a heterogeneous environment. Finally, we will try to implement code for a couple
of microservices of our sample project, leveraging all of the insights we have learned
so far.
96 
| 
Chapter 5: Dealing with the Data
```
[^86]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.111)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.111, lines 3–10)*:
```
ever system we use for query indices may get consistency wrong, but they are not
authoritative sources, so we can always re-index from the event store, if need be. In a
way, this allows us to, indeed, have the best of both worlds.
The second major benefit of the Event Sourcing and CQRS approach is related to
auditability. When we use a relational data model, we do in-place updates. For
instance, if we decide that the customer’s address or phone number is wrong we will
update it in the corresponding table. But what happens if the customer later disputes
their record? With a relational model, we may have lost the history and find ourselves
```
[^87]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.106)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.106, lines 8–15)*:
```
give us state based on events, and they’re also fairly simple. To run a projection, we
need a projection function. A projection function takes the current state and a new
event to calculate the new state.
For instance, a priceUp projection function, for an airline ticket price, may look like
the following:
function priceUp(state, event) {
  state.increasePrice(event.amount)
}
```
[^88]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Functional Programming** *(p.106)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.106, lines 26–33)*:
```
let price = priceUp(priceUp(priceDown(s,e),e),e);
If you have ever worked with functional programming, you may notice that the cur‐
rent state is the left fold of the events that occurred until the current time. Note that
through using Event Sourcing you can calculate not just the current state but the state
as of any point in time. This capability opens up endless possibilities for sophisticated
analytics, where you can ask questions like, “OK, I know what the state of the entity is
now, but what was the state at a date in the past that I am interested in?” This flexibil‐
ity can become one of the powerful benefits of using Event Sourcing, if you frequently
```
[^89]
**Annotation:** This excerpt demonstrates 'functional programming' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Global** *(p.105)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.105, lines 17–24)*:
```
First, the event needs some kind of unique identifier. You could for instance use a
universally unique identifier (UUID), since they are globally unique, and this unique‐
ness obviously helps in distributed systems. It also needs to have an event type, so we
don’t mistake different event types. And then there’s just data, whatever data is rele‐
vant for that event type:
{
  "eventId" : "afb2d89d-2789-451f-857d-80442c8cd9a1",
  "eventType" : "priceIncreased",
```
[^90]
**Annotation:** This excerpt demonstrates 'global' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Immutability** *(p.115)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.115, lines 16–23)*:
```
easier.
The immutable infrastructure principle is an application of this immutability prop‐
erty on infrastructure components. Suppose we were to set up and install a network
load balancer with a set of defined routes. If we apply the immutability principle, the
network routes we’ve defined can’t be changed without destroying the load balancer
and making a new one.
The main advantage of applying immutability here is to create predictable and easily
reproducible infrastructures. In traditional systems, human operators need to do a lot
```
[^91]
**Annotation:** This excerpt demonstrates 'immutability' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Immutable** *(p.115)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.115, lines 2–9)*:
```
structure platform:
• Immutable infrastructure
• IaC
• CI and CD
Let’s take a look at each of these ideas in more detail to understand how they’ll help
us, starting with the principle of immutable infrastructure.
Immutable Infrastructure
An object is immutable if it can’t be changed after it’s created. The only way to update
```
[^92]
**Annotation:** This excerpt demonstrates 'immutable' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 6: Service Communication** *(pp.135–178)*

This later chapter builds upon the concepts introduced here, particularly: as, class, def.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^93]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, class appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Working with Data** *(pp.179–208)*

This later chapter builds upon the concepts introduced here, particularly: None, as, def.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^94]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Running Microservices** *(pp.209–242)*

This later chapter builds upon the concepts introduced here, particularly: as, class, close.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^95]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, class appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 6: Service Communication

*Source: Microservices Up and Running, pages 135–178*

### Chapter Summary
Explores communication patterns between microservices including synchronous and asynchronous approaches. Covers REST, RPC, messaging systems, event-driven architecture, choreography vs orchestration, API gateways, service mesh, load balancing, and resilience patterns like circuit breakers and retry logic. [^96]

### Concept-by-Concept Breakdown
#### **As** *(p.153)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.153, lines 1–8)*:
```
CHAPTER 7
Building a Microservices Infrastructure
In the previous chapter we built a CI/CD pipeline for infrastructure changes. The
infrastructure for our microservices system will be defined in code and we’ll be able
to use the pipeline to automate the testing and implementation of that code. With our
automated pipeline in place, we can start writing the code that will define the infra‐
structure for our microservices-based application. That’s what we’ll focus on in this
chapter.
```
[^97]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 19 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.172)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.172, lines 1–8)*:
```
It’s good practice to include a description attribute for every vari‐
able in your Terraform module. This improves the maintainability
and usability of your modules and becomes increasingly important
over time. We’ve done this for the Terraform files we’ve published
in GitHub, but we’ve removed the descriptions in all our examples
to save space in the book.
The Terraform code for our network module is now complete. At this point, you
should have a list of files that looks something like this in your module directory:
```
[^98]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.153)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.153, lines 9–16)*:
```
Setting up the right infrastructure is vital to getting the most out of your microservi‐
ces system. Microservices give us a nice way of breaking the parts of our application
into bite-sized pieces. But we’ll need a lot of supporting infrastructure to make all
those bite-sized services work together properly. Before we can tackle the challenges
of designing and engineering the services themselves, we’ll need to spend some time
establishing a network architecture and a deployment architecture for the services to
use.
By the end of this chapter, you’ll have built a cloud-based infrastructure designed to
```
[^99]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.164)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.164, lines 3–10)*:
```
block and a set of descriptive tags.
Classless inter-domain routing (CIDR) is a standard way of describing an IP address
range for the network. It’s a shorthand string that defines which IP addresses are
allowed inside a network or a subnet. For example, a CIDR value of 10.0.0.0/16
would mean that you could bind to any IP address between 10.0.0.0 and 10.0.255.255
inside the VPC. We’ll be defining a pretty standard CIDR range for you when we
build the sandbox environment, but for more details on how CIDRs work and why
they exist, you can read about them in the RFC.
```
[^100]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.172)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.172, lines 32–39)*:
```
module-aws-network$ terraform init
If you run into any problems, try to fix those before you continue; the Terraform doc‐
umentation has a helpful section on troubleshooting. Finally, you can run the vali
date command to make sure that our module is syntactically correct:
module-aws-network$ terraform validate
Success! The configuration is valid.
156 
| 
```
[^101]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.164)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.164, lines 1–8)*:
```
After the local variable declaration, you’ll find the code for creating a new AWS VPC.
As you can see, there isn’t much to it, but it does define two important things: a CIDR
block and a set of descriptive tags.
Classless inter-domain routing (CIDR) is a standard way of describing an IP address
range for the network. It’s a shorthand string that defines which IP addresses are
allowed inside a network or a subnet. For example, a CIDR value of 10.0.0.0/16
would mean that you could bind to any IP address between 10.0.0.0 and 10.0.255.255
inside the VPC. We’ll be defining a pretty standard CIDR range for you when we
```
[^102]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 12 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.143)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.143, lines 35–39)*:
```
The steps collection indicates the specific workflow steps that the workflow will per‐
form within the environment we have set up. But before we do anything else we need
Building an IaC Pipeline 
| 
127
```
[^103]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.147)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.147, lines 5–12)*:
```
command so that there won’t be any need for human interaction.
We’re almost done with the pipeline. The final step is to publish any files that we want
to keep from our run.
Publishing assets and committing changes
When a GitHub Actions workflow completes, the VM that we used for our build is
destroyed. But sometimes we want to keep some of the state, files, or results for later
use. To help with that, GitHub provides an upload-artifact action that gives us an
easy way to make files available for us to download later.
```
[^104]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 11 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.137)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.137, lines 20–27)*:
```
bucket to store our backend state. It also defines a set of local variables using a Terra‐
form construct called locals. Finally, it has a few Terraform comments at the end,
indicating where we’ll be adding details for the infrastructure. We’ll be using the local
variables and filling in the rest of the configuration in the next chapter. For now, we
just want to test the scaffolding of our Terraform file.
With our first Terraform code file written, we’re ready to try running some Terraform
commands to make sure it works as expected. The Terraform CLI tool includes a lot
of helpful features to improve the quality and safety of your infrastructure code. You
```
[^105]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.147)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.147, lines 1–8)*:
```
As you can see from your YAML, we’re using the run action to call the Terraform CLI
from the Ubuntu shell. This is largely the same as what you did in your local environ‐
ment with the addition of the apply step at the end that will make real changes in the
AWS infrastructure. Notice that we’ve added the -auto-approve flag to the apply
command so that there won’t be any need for human interaction.
We’re almost done with the pipeline. The final step is to publish any files that we want
to keep from our run.
Publishing assets and committing changes
```
[^106]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.136)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.136, lines 7–14)*:
```
Modules
Terraform modules are similar to functions or procedures in a regular program‐
ming language. They give you a nice way of encapsulating your HCL code in a
reusable, modular way.
There’s a lot more to Terraform that what we’ve described here, but this is enough
knowledge for us to get started with our environment build work. If you want to go
deeper, the Terraform documentation is a great place to start.
Our next step is to write some Terraform code that will help us build a sandbox envi‐
```
[^107]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Global** *(p.174)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.174, lines 33–40)*:
```
# GitOps Configuration
Amazon’s S3 bucket names must be globally unique, so you’ll need
to change the value of bucket to something that is unique and
meaningful for you. Refer to “Creating an S3 Backend for Terra‐
form” on page 115 for instructions on how to set up the backend. If
you want to do a quick and dirty test, omit the backend definition
and Terraform will store state locally in your filesystem.
158 
```
[^108]
**Annotation:** This excerpt demonstrates 'global' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Immutable** *(p.151)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.151, lines 6–13)*:
```
DevOps principles and practices. We installed and used Terraform as our tool for
implementing the principles of IaC and immutable infrastructure. We set up a
GitHub-based code repository to manage that code. Finally, we created a GitHub
Actions workflow as a CI/CD pipeline with automated testing to improve the safety
and speed of our infrastructure changes.
We didn’t actually create any infrastructure resources, but we did walk through the
steps of making an infrastructure change. We created and edited a Terraform file, tes‐
ted and ran it locally, committed it to the repository, and tagged it to kick off a build
```
[^109]
**Annotation:** This excerpt demonstrates 'immutable' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.161)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.161, lines 1–8)*:
```
We recommend that you make these repositories public so that they are easier to
import into your Terraform environment definition. You can use private repositories
if you prefer—you’ll just have to add some authentication information to your import
command so that Terraform can get to the files correctly. You should also add
a .gitignore file to these repositories so you don’t end up with a lot of Terraform work‐
ing files pushed to your GitHub server. You can do that by choosing a Terra‐
form .gitignore in the GitHub web GUI, or save the contents as a .gitignore file in the
root directory of your code repository, as outlined on this GitHub site.
```
[^110]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Instance** *(p.158)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.158, lines 10–17)*:
```
environment ready for the infrastructure build. So you’ll have:
• An AWS instance and a configured operator account
• Git, Terraform, and AWS CLI tools installed in your workstation
• A GitHub Actions pipeline for the infrastructure
If you haven’t yet set up your GitHub Actions pipeline, or you had trouble getting it
to work the way we’ve described, you can create a fork of a basic sandbox environ‐
ment by following the instructions in this book’s GitHub repository.
In addition to the setup we’ve done in the previous chapter, you’ll need to do one
```
[^111]
**Annotation:** This excerpt demonstrates 'instance' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 7: Working with Data** *(pp.179–208)*

This later chapter builds upon the concepts introduced here, particularly: as, break, continue.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^112]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Running Microservices** *(pp.209–242)*

This later chapter builds upon the concepts introduced here, particularly: as, break, class.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^113]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Operating Microservices** *(pp.243–266)*

This later chapter builds upon the concepts introduced here, particularly: as, continue, def.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^114]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, continue appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 7: Working with Data

*Source: Microservices Up and Running, pages 179–208*

### Chapter Summary
Addresses data management challenges in microservices including distributed data patterns, database per service approach, eventual consistency, saga pattern for distributed transactions, event sourcing, CQRS, data synchronization strategies, polyglot persistence, and managing data ownership boundaries. [^115]

### Concept-by-Concept Breakdown
#### **Gil** *(p.204)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.204, lines 32–39)*:
```
everything you already have set up. You have to be careful, since this process can be
fragile, but generally speaking, you need to stop a Multipass process via launchctl
(otherwise it will overwrite your changes) and edit the configuration JSON, then
relaunch the Multipass process:
→ sudo launchctl unload /Library/LaunchDaemons/com.canonical.multipassd.plist
→ sudo vi "/var/root/Library/Application
  Support/multipassd/multipassd-vm-instances.json"
→ sudo launchctl load /Library/LaunchDaemons/com.canonical.multipassd.plist
```
[^116]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.192)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.192, lines 14–21)*:
```
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   172.20.0.1   <none>        443/TCP   2h
This shows us that our network and EKS services were provisioned and we were able
to successfully connect to the cluster. To get this information, kubectl makes an API
call to the Kubernetes cluster we’ve just created. Getting this response back is proof
that our cluster is up and running. As a final test, we’ll check to make sure that Argo
CD has been installed in the cluster. Run the following command to verify that the
Argo CD pods are running:
```
[^117]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.188)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.188, lines 11–18)*:
```
    command     = "aws-iam-authenticator"
    args        = ["token", "-i", "${var.kubernetes_cluster_name}"]
  }
}
provider "helm" {
  kubernetes {
    load_config_file       = false
    cluster_ca_certificate = base64decode(var.kubernetes_cluster_cert_data)
```
[^118]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.204)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.204, lines 1–8)*:
```
Installing Multipass
Multipass installers for various platforms can be downloaded from the website. Once
you have it installed, check out the following interesting things you can do on macOS
or Windows Subshell for Linux.
To launch a new Ubuntu environment:
→ multipass launch -n docker
Launched: docker
→ multipass list
```
[^119]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 24 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.203)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.203, lines 22–29)*:
```
a problem that Docker4Mac only allows you to install one Docker instance and one
Kubernetes. If you experiment a lot, you may want to have more freedom to break
things.
Thankfully, there are alternatives. The obvious one is to install your own VMs with
VirtualBox or its commercial alternatives. My experience, however, has been that
these are even heavier than Docker4Mac/Win packages.
One of the more interesting alternatives that I have recently started experimenting
with, however, is Multipass, a slick tool from Canonical, the creators of Ubuntu, that
```
[^120]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.187)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.187, lines 17–24)*:
```
As we mentioned earlier, we’re going to complete our infrastructure setup with a
GitOps server that we’ll use later in the book. We’ll continue to follow the module
pattern by creating a Terraform module for Argo CD that we can call to bootstrap the
server in our sandbox environment. Unlike the other modules, we’ll be installing
Argo CD on the Kubernetes system that we’ve just instantiated.
To do that, we’ll need to let Terraform know that we’re using a different host. Up until
now, we’ve been using the AWS provider, which lets Terraform communicate with
AWS through its API. For our Argo CD installation we’ll use a Kubernetes provider;
```
[^121]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.180)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.180, lines 1–8)*:
```
With these policies and a security group defined for the EKS cluster, we can now add
the declaration for the cluster itself to the main.tf Terraform file (see Example 7-13).
Example 7-13. module-aws-kubernetes/main.tf (cluster definition)
resource "aws_eks_cluster" "ms-up-running" {
  name     = local.cluster_name
  role_arn = aws_iam_role.ms-cluster.arn
  vpc_config {
    security_group_ids = [aws_security_group.ms-cluster.id]
```
[^122]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Development Speed** *(p.197)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.197, lines 13–20)*:
```
dard tech stacks is a powerful way of achieving such consistency and high quality,
while also increasing development speed.
Quality control must be automated
Enforcement of a company’s software development quality standards must be
automated and not left to human error.
Based on these goals, we can derive a set of fundamental guidelines for a developer
workspace setup.
10 Workspace Guidelines for a Superior Developer Experience
```
[^123]
**Annotation:** This excerpt demonstrates 'development speed' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.197)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.197, lines 31–38)*:
```
code, we should only expect to see the Docker runtime and Docker Compose on
the host machine—nothing else! It should not matter if the machine is running
Windows, macOS, or Linux and what libraries are present. Such assumptions are
exactly what lead to broken setups. For instance, there should be no set expecta‐
tions about a specific version of Python, Go, Java, etc., being present on the
developer’s machine. Setup instructions must be automated, not codified in
READ.ME files.
Coding Standards and the Developer’s Setup 
```
[^124]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Except** *(p.195)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.195, lines 13–20)*:
```
your developers.
Investing in an exceptional developer experience that aims at a
consistent and intuitive approach for all developers to easily “do the
right thing” is one of the most underappreciated prerequisites of
facilitating a successful microservices culture.
This is why developing robust continuous integration and continuous deployment
(CI/CD) pipelines, for both your code as well as infrastructure, is a key enabler for
your microservices efforts. Because of the modular nature of the architecture and the
```
[^125]
**Annotation:** This excerpt demonstrates 'except' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Exception** *(p.195)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.195, lines 13–20)*:
```
your developers.
Investing in an exceptional developer experience that aims at a
consistent and intuitive approach for all developers to easily “do the
right thing” is one of the most underappreciated prerequisites of
facilitating a successful microservices culture.
This is why developing robust continuous integration and continuous deployment
(CI/CD) pipelines, for both your code as well as infrastructure, is a key enabler for
your microservices efforts. Because of the modular nature of the architecture and the
```
[^126]
**Annotation:** This excerpt demonstrates 'exception' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.183)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.183, lines 1–8)*:
```
Example 7-16. module-aws-kubernetes/main.tf (generate kubeconfig)
# Create a kubeconfig file based on the cluster that has been created
resource "local_file" "kubeconfig" {
  content  = <<KUBECONFIG_END
apiVersion: v1
clusters:
- cluster:
    "certificate-authority-data: >
```
[^127]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 11 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.194)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.194, lines 20–27)*:
```
module that instantiates an AWS EKS cluster for Kubernetes. We also implemented
an Argo CD GitOps server into the cluster using a Helm package. Finally, we imple‐
mented a sandbox environment as code that uses all of these modules in a declarative,
immutable way.
We went into a lot of detail with the Terraform code in this chapter. We did that so
you could get a feel for what it takes to define an environment using infrastructure as
code, immutability, and a CI/CD pipeline. We also wanted you to get hands on with
the Terraform module pattern and some of the design decisions you’ll need to make
```
[^128]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.183)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.183, lines 35–42)*:
```
populating kubeconfig with YAML content that defines the connection parameters for
our Kubernetes cluster. Notice that we are getting the values for the YAML file from
the EKS resources that we created in the module.
When Terraform runs this block of code, it will create a kubeconfig file in a local
directory. We’ll be able to use that file to connect to the Kubernetes environment
from CLI tools. We made a special provision for this file when we built our pipeline
in Chapter 6. When you run the infrastructure pipeline, you’ll be able to download
this populated configuration file and use it to connect to the cluster. This configura‐
```
[^129]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.196)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.196, lines 17–24)*:
```
database in the newly minted Docker setup.
By the end of this chapter, you should have a fully functioning, containerized infra‐
structure that’s ready for writing some microservices code. More importantly, you will
gain a solid understanding of the principles we use to set up projects for easy and
intuitive development. We will use these principles in Chapter 9 to properly lay out
our code, when we get into the development phase of our implementation.
Coding Standards and the Developer’s Setup
When trying to introduce any organizational standards, it’s useful to clarify and agree
```
[^130]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 8: Running Microservices** *(pp.209–242)*

This later chapter builds upon the concepts introduced here, particularly: args, as, break.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^131]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts args, as appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Operating Microservices** *(pp.243–266)*

This later chapter builds upon the concepts introduced here, particularly: as, continue, def.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^132]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, continue appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: Microservices Organizational Impact** *(pp.267–282)*

This later chapter builds upon the concepts introduced here, particularly: as, break, def.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^133]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 8: Running Microservices

*Source: Microservices Up and Running, pages 209–242*

### Chapter Summary
Details running and deploying microservices in production. Covers containerization with Docker, Kubernetes orchestration, cloud deployment strategies, CI/CD automation pipelines, release strategies including rolling deployments, blue-green deployments, canary releases, and implementing immutable infrastructure. [^134]

### Concept-by-Concept Breakdown
#### **__Name__** *(p.238)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.238, lines 38–45)*:
```
adding the following code around line 19 of src/models.py, right after the this =
sys.modules[__name__] declaration:
this = sys.modules[__name__] # Existing line
this.tblprefix = "flights:" # New line
The microservice template we used readily contains all of the code required to grab
the relevant credentials and configuration from the environment and connect to a
222 
| 
```
[^135]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.240)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.240, lines 31–38)*:
```
    """ Get Reservations Endpoint"""
    flight_id = request.args.get('flight_id')
    resp = handlers.get_reservations(flight_id)
    return jsonify(resp)
The implementation of the handler in src/handlers.py will again be simple since we
are skipping input validation, for the sake of brevity:
def get_reservations(flight_id):
    """Get reservations callback"""
```
[^136]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.235)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.235, lines 6–13)*:
```
yet or is down, it won’t be actually ready for useful work.
The fourth argument {minCacheMs: 10000} in the .addCheck() call sets minimal
cache duration on the server side, indicated in milliseconds. This means you can tell
the health-check middleware (the module we use) to only run an expensive, database-
querying health-check probe against MySQL every 10 seconds (10,000 milliseconds),
at most!
Even if your health-probing infrastructure (e.g., Kubernetes) calls your health-check
endpoint very frequently, the middleware will only trigger the calls you deemed light
```
[^137]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.220)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.220, lines 15–22)*:
```
                    Cabin:
                      type: array
                      items:
                        type: object
                        properties:
                          firstRow:
                            type: number
                            example: 8
```
[^138]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.209)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.209, lines 1–8)*:
```
Creating cassandra-seed ... done
ubuntu@dubuntu:~/cassandra$ docker-compose ps
Name                   Command               State             Ports
-------------------------------------------------------------------------------
cassandra-seed   docker-entrypoint.sh cassa ...   Up      7000/tcp, 7001/tcp
ubuntu@dubuntu:~/cassandra$ docker exec -it cassandra-seed cqlsh
Connected to Test Cluster at 127.0.0.1:9042.
[cqlsh 5.0.1 | Cassandra 3.11.6 | CQL spec 3.4.4 | Native protocol v4]
```
[^139]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 17 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.235)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.235, lines 18–25)*:
```
query so that lines 7–10 read:
async dbCheck() {
  const start = new Date();
  const conn = await db.conn();
  const query = 'select count(1) from seat_maps';
If everything was done correctly and the microservice is up and running in a healthy
way, if you now run curl http://0.0.0.0:5501/health, you should get a health
endpoint output that looks like the following:
```
[^140]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.235)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.235, lines 20–27)*:
```
  const start = new Date();
  const conn = await db.conn();
  const query = 'select count(1) from seat_maps';
If everything was done correctly and the microservice is up and running in a healthy
way, if you now run curl http://0.0.0.0:5501/health, you should get a health
endpoint output that looks like the following:
{
  "details": {
```
[^141]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.221)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.221, lines 17–24)*:
```
                                      premiumInd:
                                        type: boolean
                                        example: false
                                      exitRowInd:
                                        type: boolean
                                        example: false
                                      restrictedReclineInd:
                                        type: boolean
```
[^142]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.241)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.241, lines 33–40)*:
```
get a better feel for what you get from the template this code was bootstrapped from.
You should also use this opportunity to take a break and pat yourself on the back—
you just created and executed two perfectly sized, impeccably implemented, and
beautifully separate-stack microservices! Hooray!
Now what we need to do is figure out a way to execute these two microservices (and
any additional future components you may create) as a single unit. For this, we will
introduce the notion of an “umbrella project” and explain how to develop one.
Introducing a Second Microservice to the Project 
```
[^143]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.210)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.210, lines 15–22)*:
```
cific group, and will need to log in again just like we did with Docker:
ubuntu@dubuntu:~$ sudo snap install microk8s --classic
microk8s v1.18.1 from Canonical✓ installed
ubuntu@dubuntu:~$ sudo usermod -a -G microk8s $USER
ubuntu@dubuntu:~$ sudo chown -f -R $USER ~/.kube
ubuntu@dubuntu:~$ exit
logout
→ multipass shell
```
[^144]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.217)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.217, lines 29–34)*:
```
As discussed in Chapter 3, the beauty of writing down actions and queries is that they
bring us much closer to being able to create the technical specifications of the services
than when jobs are presented in their business-oriented, jobs (JTBD) format.
Designing Microservice Endpoints 
| 
201
```
[^145]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Datetime** *(p.227)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.227, lines 14–21)*:
```
Additionally, in the lookup endpoint we need to query data by two fields: flight_no
and datetime. A relational database is a more natural structure for such queries. In
Redis, we would probably need to create a compound field to achieve the same. All in
all, while we could technically implement this service with Redis as well, there are
reasons to choose MySQL for doing this, among them that MySQL also helps us
demonstrate usage of different databases for different services. Real-life situations will
obviously be more complex, with more aspects to consider.
Let’s look at the seat_maps table:
```
[^146]
**Annotation:** This excerpt demonstrates 'datetime' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Debugging** *(p.229)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.229, lines 8–15)*:
```
the commands you issue will execute inside the containers, but there’s rarely a need
for you to explicitly shell into the containers, unless you are debugging something 
low level.
The Code Behind the Flights Microservice
To use NodeBootstrap for jump-starting a Node/Express microservice, either install
its bootstrapper with node install -g nodebootstrap (if you already have Node
available on your system), or clone this GitHub template repository.
While the former may be somewhat easier, we will do the latter since we do not want
```
[^147]
**Annotation:** This excerpt demonstrates 'debugging' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.240)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.240, lines 25–32)*:
```
Since we now have some data in the Redis store, we can proceed to implementing the
reservation retrieval endpoint as well. Again, we will start with the mapping defini‐
tion in service.py, replacing the default /hello/<name> greeter endpoint with the
following:
@app.route('/reservations', methods=['GET'])
def reservations():
    """ Get Reservations Endpoint"""
    flight_id = request.args.get('flight_id')
```
[^148]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.238)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.238, lines 18–25)*:
```
        log.error(f"Unexpected error reserving {seat_num}", exc_info=True)
    else:
        if result == 1:
            response = {
                "status": "success",
            }
        else:
            response = {
```
[^149]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 9: Operating Microservices** *(pp.243–266)*

This later chapter builds upon the concepts introduced here, particularly: as, def, else.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^150]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, def appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: Microservices Organizational Impact** *(pp.267–282)*

This later chapter builds upon the concepts introduced here, particularly: as, break, class.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^151]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Adopting Microservices** *(pp.283–302)*

This later chapter builds upon the concepts introduced here, particularly: as, break, class.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^152]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 9: Operating Microservices

*Source: Microservices Up and Running, pages 243–266*

### Chapter Summary
Focuses on operating microservices in production including observability practices, monitoring, centralized logging, distributed tracing, metrics collection, alerting strategies, health checks, dashboards, incident response procedures, debugging distributed systems, and defining SLOs and SLAs for reliability. [^153]

### Concept-by-Concept Breakdown
#### **As** *(p.250)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.250, lines 1–8)*:
```
We’ll get a chance to use this ingress module in “Forking the Staging Infrastructure
Project” on page 234 when we build the staging environment. For now, let’s see how
we’ll support our database needs.
The Database Module
Each of our microservices use different databases, so we’ll need to provision two dif‐
ferent databases in the infrastructure environment. We’ll need both a MySQL and a
Redis database to support the needs of our microservices teams. For our build, we’ve
decided to use AWS managed versions of these database products. That way, our plat‐
```
[^154]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 25 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.250)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.250, lines 24–31)*:
```
The staging environment we need for releasing our microservices will be very similar
to the sandbox environment we created in Chapter 7. We’ll continue to use the same
methods and principles we applied earlier. We’ll use Terraform to define the environ‐
ment in code and we’ll use the modules we wrote for the network, Kubernetes cluster,
and Argo CD. We’ll complement those modules with the new database and ingress
controller modules we’ve just described. Finally, we’ll use a GitHub Actions pipeline
to provision the environment, just like we did for our sandbox environment.
We explained how to create a GitHub Actions pipeline in Chapter 6, and walked
```
[^155]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.264)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.264, lines 5–12)*:
```
Service
A Service defines how applications in the Kubernetes cluster can access this Pod
over the network—even when there are multiple replicas running at the same
time. The Service object lets you define a single IP and port for accessing a
group of replicated Pods. You’ll almost always want to define a service for a
microservice deployment.
Ingress
The Ingress object allows you to identify an ingress route to your Service for
```
[^156]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.251)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.251, lines 3–10)*:
```
Figure 10-4. Starting with the staging environment repository
In GitHub, a fork lets you make a copy of someone else’s code project in your own
account. To fork the staging environment repository, follow these steps:
1. Open your browser and sign in to your GitHub account.
2. Navigate to this book’s GitHub repository.
3. Click the Fork button in the top-right corner of the screen.
You may want to duplicate this repository instead of forking it.
This will allow you to change the access mode of the repository to
```
[^157]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.253)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.253, lines 1–8)*:
```
The staging workflow we’ve built for you will automatically gener‐
ate a kubeconfig file as part of the provisioning process. This file
contains connection information so you can connect to the Kuber‐
netes cluster that we’ll create on EKS. Since this code repository is
public, that file will be available to anyone who visits your reposi‐
tory. In theory, this shouldn’t be a problem. Our EKS cluster
requires AWS credentials to authenticate and connect. That means
even with the kubeconfig file an attacker shouldn’t be able to con‐
```
[^158]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.250)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.250, lines 28–35)*:
```
and Argo CD. We’ll complement those modules with the new database and ingress
controller modules we’ve just described. Finally, we’ll use a GitHub Actions pipeline
to provision the environment, just like we did for our sandbox environment.
We explained how to create a GitHub Actions pipeline in Chapter 6, and walked
through the process of writing and using Terraform code in Chapter 7. So there’s no
need to do all of that again. Instead, we’ll use a staging environment skeleton project
that we’ve already created for you (see Figure 10-4). We’ll need to make a few small
234 
```
[^159]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.251)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.251, lines 19–26)*:
```
tials and a MySQL password to the repository’s secrets. You should have your AWS
operator account credentials from the pipeline setup work we did in Chapter 6. If you
don’t have those keys anymore, you can open the AWS management console in a
browser and create a new set of credentials for your operations user.
When you have your credentials in hand, navigate to the Settings pane of your forked
GitHub repository and choose Secrets from the lefthand navigation menu. Add the
secrets in Table 10-1 by clicking the New secret button.
Setting Up the Staging Environment 
```
[^160]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.256)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.256, lines 23–30)*:
```
mysql --from-literal=password=microservices -n microservices
The built-in secrets functions of Kubernetes are useful, but we rec‐
ommend that you use something more feature rich for a proper
implementation. There are lots of options available in this area,
including HashiCorp Vault.
We now have a staging environment with an infrastructure that fits the needs of the
microservices we’ve developed. The next step will be to publish those microservices
as containers so that we can deploy them into the environment.
```
[^161]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Immutable** *(p.249)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.249, lines 1–8)*:
```
• An AWS-based Redis database instance for the reservations microservice’s data
This kind of nontrivial change could be risky. But this is where our immutable infra‐
structure and infrastructure as code (IaC) approach really starts to pay off! We know
exactly what our current environment build looks like, because all of it is in our Ter‐
raform code. All we need to do now is create modules for each of these new compo‐
nents, update an environment definition, and run the build through our CI/CD
pipeline.
In Chapter 7, we walked through the process of writing each Terraform module
```
[^162]
**Annotation:** This excerpt demonstrates 'immutable' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.264)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.264, lines 28–35)*:
```
own Helm package so we can install our microservices just as easily.
To use Helm, we’ll first need to understand the three important concepts of charts,
templates, and values:
Charts
A chart is a bundle of files that describe a Kubernetes resource or deployment.
The chart is the core unit of deployment in Helm. We used pre-made charts ear‐
lier in the book when we deployed Kubernetes-based applications like Argo CD.
248 
```
[^163]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Instance** *(p.250)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.250, lines 14–21)*:
```
In our database module, we’ll use the AWS ElastiCache service to provision a Redis
data store and the AWS Relational Database (RDS) to provision a MySQL instance.
We’ve already written a module that does this, which you can find in this book’s Git‐
Hub repository. The module provisions both types of databases as well as the net‐
work configuration and access policies that the database service needs for operation.
When the module is applied to the staging environment, we’ll have both a Redis and a
MySQL database instance running and ready for use. All that’s left now is to use our
modules in a Terraform code file and provision an environment. That’s what we’ll
```
[^164]
**Annotation:** This excerpt demonstrates 'instance' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Json** *(p.243)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.243, lines 4–11)*:
```
col so you can modify them.
Now that we have configured repos.json, let’s pull the ms-flights and ms-reservations
microservices into the workspace:
→ make update
git clone -b master \
  https://github.com/implementing-microservices/ms-flights ms-flights
Cloning into 'ms-flights'...
git clone -b master \
```
[^165]
**Annotation:** This excerpt demonstrates 'json' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **List** *(p.256)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.256, lines 10–17)*:
```
[... lots more services ...]
In the result you should see a list of all the Kubernetes services that we’ve deployed.
That should include services for the Argo CD application and the Nginx ingress ser‐
vice. That means that our cluster is up and running and the services we need have
been successfully provisioned.
Create a Kubernetes secret
The last step we need to take care of is setting up a Kubernetes secret. When our flight
information microservices connects to MySQL, it will need a password. To avoid
```
[^166]
**Annotation:** This excerpt demonstrates 'list' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Method** *(p.245)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.245, lines 5–12)*:
```
to work on these services either individually or as a unified project. We did this
through a step-by-step implementation of the powerful SEED(S) methodology and
the design of individual data models, and learned how to quickly jump-start code
implementations from robust template projects.
The ability to put together well-modularized components quickly and efficiently can
make a material difference in your ability to execute microservice projects success‐
fully. There’s a big difference between what you were able to achieve in this chapter,
and somebody spending weeks figuring out the basic boilerplate or going down the
```
[^167]
**Annotation:** This excerpt demonstrates 'method' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Module** *(p.250)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.250, lines 1–8)*:
```
We’ll get a chance to use this ingress module in “Forking the Staging Infrastructure
Project” on page 234 when we build the staging environment. For now, let’s see how
we’ll support our database needs.
The Database Module
Each of our microservices use different databases, so we’ll need to provision two dif‐
ferent databases in the infrastructure environment. We’ll need both a MySQL and a
Redis database to support the needs of our microservices teams. For our build, we’ve
decided to use AWS managed versions of these database products. That way, our plat‐
```
[^168]
**Annotation:** This excerpt demonstrates 'module' as it appears in the primary text. The concept occurs 11 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 10: Microservices Organizational Impact** *(pp.267–282)*

This later chapter builds upon the concepts introduced here, particularly: as, def, file.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^169]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, def appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Adopting Microservices** *(pp.283–302)*

This later chapter builds upon the concepts introduced here, particularly: as, continue, def.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^170]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, continue appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 12: Microservices: The Future** *(pp.303–319)*

This later chapter builds upon the concepts introduced here, particularly: as, def, file.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^171]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, def appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 10: Microservices Organizational Impact

*Source: Microservices Up and Running, pages 267–282*

### Chapter Summary
Examines organizational impact of microservices including team structures, Conway's Law implications, DevOps culture, service ownership models, cross-functional team design, team autonomy, governance approaches, effective collaboration patterns, skill development, and organizational alignment strategies. [^172]

### Concept-by-Concept Breakdown
#### **Annotation** *(p.270)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.270, lines 2–9)*:
```
  enabled: true
  annotations:
    kubernetes.io/ingress.class: traefik
  hosts:
    - host: flightsvc.com
      paths: ["/flights"]
This definition lets our Ingress service know that it should route any messages sent to
the host flightsvc.com with a URI of /flights to the flight information microservice. We
```
[^173]
**Annotation:** This excerpt demonstrates 'annotation' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.280)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.280, lines 3–10)*:
```
• Integrating with a new partner
These are all important reasons to change and our architecture should facilitate these
kinds of changes to make them as cost-effective as possible. But it’s important to
understand that the microservices style is an optimization technique. That means we
should consider intrinsic drivers as well. The following changes come from our
observation of the system itself:
• Splitting a microservice to reduce code complexity
• Redeploying infrastructure to avoid drifting from the infrastructure code
```
[^174]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 13 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.282)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.282, lines 15–22)*:
```
example, a change to an infrastructure module may have wide-reaching impact
on microservice developer teams. Similarly, a change to an interface can break
the code of every component that uses it.
Software architecture has a big role to play in the costs and impacts of change across
all four of the lenses we’ve described. But another part of the story is the way that
changes are applied. Microservices architectures, cloud infrastructures, and DevOps
practices have enabled practices that are a huge leap forward. Let’s take a look at two
modern deployment patterns as well as an older one that has managed to stick
```
[^175]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.270)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.270, lines 3–10)*:
```
  annotations:
    kubernetes.io/ingress.class: traefik
  hosts:
    - host: flightsvc.com
      paths: ["/flights"]
This definition lets our Ingress service know that it should route any messages sent to
the host flightsvc.com with a URI of /flights to the flight information microservice. We
won’t need to actually host the service at the flightsvc.com domain, we’ll just need to
```
[^176]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.268)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.268, lines 35–42)*:
```
• Liveness and readiness endpoints that Kubernetes will use to check if the Pod is
still alive (as defined in Chapter 9)
That’s all we need to customize to make the generated Helm templates work for us.
With the deployment template we’ve created, we have a parameterized Kubernetes
Deployment object defined. We’ll only need to define some values to use in the
template.
252 
| 
```
[^177]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.269)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.269, lines 5–12)*:
```
did this earlier in the book when we installed the Helm package for Argo CD.
Another option is to create a file that serializes all of the values you want to use in a
single place. This is the approach we’ll take for our deployment package. This gives us
the advantage of being able to manage our deployment value files as code. We’ll use
the values.yaml file that Helm has generated for us already. You’ll find that file in the
root directory of the ms-flights chart.
First, we’ll need to update the details for the Docker image. Open the values.yaml file
in your favorite text editor and find the image key at the beginning of the YAML file.
```
[^178]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.269)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.269, lines 32–37)*:
```
MYSQLSecretKey: password
Finally, find the ingress property near the end of the YAML file and update it with
the following text:
Deploying the Flights Service Container 
| 
253
```
[^179]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.272)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.272, lines 1–8)*:
```
need to set up a port-forwarding rule. That’s because we haven’t properly defined a
way to access our Kubernetes cluster from the internet. But thankfully kubectl pro‐
vides a handy built-in tool for forwarding requests from your local machine into the
cluster. Use the following to get it running:
$ kubectl port-forward svc/msur-argocd-server 8443:443 -n "argocd"
Forwarding from 127.0.0.1:8443 -> 8080
Forwarding from [::1]:8443 -> 8080
Now you should be able to navigate to localhost:8443 in your browser. You’ll almost
```
[^180]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.280)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.280, lines 3–10)*:
```
• Integrating with a new partner
These are all important reasons to change and our architecture should facilitate these
kinds of changes to make them as cost-effective as possible. But it’s important to
understand that the microservices style is an optimization technique. That means we
should consider intrinsic drivers as well. The following changes come from our
observation of the system itself:
• Splitting a microservice to reduce code complexity
• Redeploying infrastructure to avoid drifting from the infrastructure code
```
[^181]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Instance** *(p.271)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.271, lines 19–26)*:
```
adopted, like Terraform. To make all this magic happen, we just need to log in to the
Argo CD instance that we’ve installed in staging, point to our ms-deploy repository,
and set up a synchronized deployment.
Make sure you’ve added the MySQL password Kubernetes Secret as
described in “Create a Kubernetes secret” on page 240. Otherwise,
the flight information service won’t be able to start up.
Log in to Argo CD
Before we can log in to Argo CD, we’ll need to get the password for the Argo admin‐
```
[^182]
**Annotation:** This excerpt demonstrates 'instance' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Json** *(p.276)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.276, lines 4–11)*:
```
 {TRAEFIK-EXTERNAL-IP}/flights?flight_no=AA2532
If all has gone well, you’ll get the details of that flight as a JSON-formatted response.
You can use a dedicated API testing tool such as Postman or
SoapUI to get a more user-friendly formatted version of the
response message.
The HTTP request we’ve just made calls the ingress service, which in turn routes the
message to the flights microservice based on the ingress rule we defined earlier in this
chapter. The flights microservice retrieves data from the database service we provi‐
```
[^183]
**Annotation:** This excerpt demonstrates 'json' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **List** *(p.273)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.273, lines 41–46)*:
```
for instructions on setting up an application.
If you’ve created the application successfully, Argo CD will list the flight-info applica‐
tion in the dashboard, as shown in Figure 10-14.
Deploying the Flights Service Container 
| 
257
```
[^184]
**Annotation:** This excerpt demonstrates 'list' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Method** *(p.279)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.279, lines 7–14)*:
```
built. We’ll take a look at the typical kinds of change you’ll need to do and the pat‐
terns and methods that work well to support them.
Change is an important factor because of the impact it has. Poorly designed software
can end up costing organizations a lot of pain. As we highlighted in Chapter 1, one of
the benefits of a microservices system is that it makes change faster and safer.
Also, change will always have a cost. In a software system, that cost is a combination
of time, money, and impact to people. To get the most out of our microservices sys‐
tem, we need to minimize change cost and make changes that have the greatest
```
[^185]
**Annotation:** This excerpt demonstrates 'method' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Module** *(p.282)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.282, lines 14–21)*:
```
downtime” model there can be costly impacts that could have been avoided. For
example, a change to an infrastructure module may have wide-reaching impact
on microservice developer teams. Similarly, a change to an interface can break
the code of every component that uses it.
Software architecture has a big role to play in the costs and impacts of change across
all four of the lenses we’ve described. But another part of the story is the way that
changes are applied. Microservices architectures, cloud infrastructures, and DevOps
practices have enabled practices that are a huge leap forward. Let’s take a look at two
```
[^186]
**Annotation:** This excerpt demonstrates 'module' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Namespace** *(p.273)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.273, lines 36–43)*:
```
in-cluster (https://kubernetes.default.svc)
DESTINATION Namespace
microservices
When you are done filling in the form, click the Create button.
If you run into any trouble, consult the Argo CD documentation
for instructions on setting up an application.
If you’ve created the application successfully, Argo CD will list the flight-info applica‐
tion in the dashboard, as shown in Figure 10-14.
```
[^187]
**Annotation:** This excerpt demonstrates 'namespace' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 11: Adopting Microservices** *(pp.283–302)*

This later chapter builds upon the concepts introduced here, particularly: as, break, class.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^188]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, break appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 12: Microservices: The Future** *(pp.303–319)*

This later chapter builds upon the concepts introduced here, particularly: as, class, def.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^189]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, class appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 11: Adopting Microservices

*Source: Microservices Up and Running, pages 283–302*

### Chapter Summary
Covers adopting microservices and migration strategies from monolithic systems. Discusses the strangler pattern, incremental migration approaches, legacy system modernization, risk management, adoption planning, roadmap development, pilot projects, transition strategies, refactoring approaches, and change management practices. [^190]

### Concept-by-Concept Breakdown
#### **As** *(p.286)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.286, lines 1–8)*:
```
Infrastructure change: Implementation costs
The implementation cost of making infrastructure changes is a function of how diffi‐
cult a change is to both understand and execute. This is where the investment we
made in our infrastructure design helps. Our decisions to embrace the principle of
immutable infrastructure, build a CI/CD pipeline, and write IaC combine to greatly
reduce the cost of making changes.
When it comes time for you to make an infrastructure change, you can employ a
change process that looks something like this, thanks to the tools we’ve implemented:
```
[^191]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 25 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.298)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.298, lines 1–8)*:
```
On Complexity and Simplification Using Microservices
Throughout this book we have asserted that microservices are most applicable when
utilized to implement large, complex, continuously changing systems. Intuitively, this
statement makes sense: a microservices architecture itself is not simple, so embarking
on that journey has to be worth it—maybe when it helps solve something even more
complex. But what is the nature of complexity and how exactly do microservices
decrease complexity, if at all?
A seminal work on software complexity is Fred Brooks’s 1986 article, “No Silver Bul‐
```
[^192]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.284)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.284, lines 10–17)*:
```
pleted. A classic example of this situation is when you want to change an API in a way
that will break client code. In this scenario, managing migration for all parties would
require significant coordination effort. Instead, we can keep older versions running
so that we don’t need to wait for every client to change.
There are some significant challenges to using this approach. Every version of a com‐
ponent we introduce brings added maintenance and complexity costs for our system.
Versions need to be able to run safely together and parallel versions need to be con‐
tinually maintained, supported, documented, and kept secure. That overhead can
```
[^193]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.300)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.300, lines 1–8)*:
```
were to classify monoliths and microservices in these terms, monoliths would be con‐
sidered complicated, whereas microservices would be much more aligned with the
definition of complex systems.
Another interesting classification is the notion of “easy” versus “simple.” As most
designers would passionately attest, these seemingly synonymous adjectives could not
be any more different, in the context of design. Simple things are notoriously hard to
design (think Apple’s original iPod and iMac, or a simple invention such as the com‐
puter mouse), whereas easy designs are not necessarily simple to use.
```
[^194]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.285)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.285, lines 1–8)*:
```
In this section, we’ll take a tour of the system and get a closer look at how the deci‐
sions we’ve made have impacted the changeability of the architecture. We’ll look at
change through the factors of implementation costs, coordination time, downtime,
and consumer impacts that we introduced earlier in this chapter. To make things eas‐
ier, we’ll split the architecture into three subsystems: infrastructure, microservices,
and data, considering each in turn. Let’s start by examining our infrastructure.
Infrastructure Changes
In Chapter 7, we developed a Terraform-based platform for our microservices that
```
[^195]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Comprehension** *(p.289)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.289, lines 30–35)*:
```
internally consistent and addressed specific parts of our domain. The net effect is
that code comprehension should be improved and changes can be implemented
in smaller batches with speed.
Considerations for Our Architecture 
| 
273
```
[^196]
**Annotation:** This excerpt demonstrates 'comprehension' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.283)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.283, lines 13–20)*:
```
you’d release a new canary version of the web application alongside the original web
application that continues to run.
Just like the blue-green pattern, canary deployments require traffic management and
routing logic in order to work. After deploying the new version of an application,
some traffic is routed to the new version. The traffic that hits the canary version
could be a percent of the total load or could be based on a unique header or special
identifier. However it’s done, over time more traffic is routed to the canary version
until it eventually gets promoted to full-fledged production state.
```
[^197]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.299)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.299, lines 31–38)*:
```
Microservices Quadrant
Let’s dig deeper into the subject of complexity. Systems Theory distinguishes the defi‐
nition of a complicated system and a complex system. This was further expanded
upon and popularized for decision making in the Cynefin framework. A complicated
system can be very sophisticated and hard to understand, but in its essence is predict‐
able and based on a finite number of well-defined rules. In contrast, a complex sys‐
tem is by essence nondeterministic, composed of many components that interact at a
high degree of freedom, and can consequently produce emergent behaviors. If we
```
[^198]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.295)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.295, lines 28–35)*:
```
perspective of change. As you’ve seen in this chapter, the decisions we made through‐
out this book have combined to create a profile of changeability for this system. Some
of our decisions were trade-offs that were made to optimize for certain types of
change. Other decisions were trade-offs based on the constraints of the medium of a
design in a book!
Regardless of the reasons, we’ve now been able to both build a microservices architec‐
ture and evaluate its usefulness and suitability. The only thing left to do with our
architecture is to make it even better. That’s what we’ll cover in our final chapter.
```
[^199]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.286)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.286, lines 20–27)*:
```
structure changes work in a development environment, they should work in the pro‐
duction environment as well. Finally, our automated pipeline ensures that our
infrastructure code and tests will be run in the same way consistently and repeatedly.
What we’ve done in our system is to drive variation out of the change process. With
less uncertainty for us to worry about, we can focus more on making the change
itself. Writing IaC requires a bit more up-front effort, but the payoff when it comes to
changes makes it a worthwhile investment.
Overall, the infrastructure implementation costs should be lower with our architec‐
```
[^200]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.299)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.299, lines 1–8)*:
```
it achieves its goals in accord with it. You see, you cannot eliminate essential com‐
plexity, but you can shift it: you can move essential complexity from one part of the
system into another. This would not seem like a big deal, unless different parts of the
system required different levels of effort.
Simply speaking, when building any software system there’s the implementation part
of it (the code) and the operational part of it (the deployment and orchestration). We
can make the code simpler by breaking it up into many small microservices. Such
change will make your operations equally harder. It would seem that we haven’t
```
[^201]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.284)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.284, lines 1–8)*:
```
the new function until it’s safe to use. The routing decision is implicit and hidden
from users of the system.
The multiple versions pattern makes changes more transparent to the users and cli‐
ents of the system. In this deployment pattern we explictly version a component or
interface and allow clients to choose which version of the component they want to
use. In this way, we can support the use of multiple versions at the same time.
The main reason to employ this technique is if we’re making a change that will
require a dependent system to make a change as well. We use this pattern when we
```
[^202]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Global** *(p.294)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.294, lines 15–22)*:
```
We’ve optimized our architecture for high-speed, autonomous local changes. This
made system-wide changes more costly. For example, if you need to globally change
the definition of an airline identifier code, you’ll need to coordinate across all of the
teams who have implemented a data model that uses it. In our architecture, that could
be more costly than if we had just used a shared database.
A good resource for understanding distributed data patterns is
Martin 
Kleppmann’s 
```
[^203]
**Annotation:** This excerpt demonstrates 'global' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Immutable** *(p.286)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.286, lines 4–11)*:
```
made in our infrastructure design helps. Our decisions to embrace the principle of
immutable infrastructure, build a CI/CD pipeline, and write IaC combine to greatly
reduce the cost of making changes.
When it comes time for you to make an infrastructure change, you can employ a
change process that looks something like this, thanks to the tools we’ve implemented:
1. Decide on the infrastructure change you want to make.
2. Identify the infrastructure code you need to change (e.g., do you need to create a
new Terraform module? Are you just updating an environment definition?).
```
[^204]
**Annotation:** This excerpt demonstrates 'immutable' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.301)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.301, lines 16–23)*:
```
Having discussed the nature of microservices architectures through the lens of com‐
plexity, we would like to give the reader another important perspective: how to think
about a microservice transformation over time.
In Chapter 11, we discussed both the role microservices architecture plays in helping
teams tackle change in complex systems and techniques to manage change when
implementing microservices. There is another important aspect of change in regards
to microservices: the transformation that an organization as a whole needs to go
through when transitioning from a nonmicroservices culture and adopting this novel
```
[^205]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 12: Microservices: The Future** *(pp.303–319)*

This later chapter builds upon the concepts introduced here, particularly: as, assert, class.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^206]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts as, assert appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 12: Microservices: The Future

*Source: Microservices Up and Running, pages 303–319*

### Chapter Summary
Explores the future of microservices including emerging trends and technologies. Covers serverless computing, edge computing, service mesh evolution, WebAssembly, AI/ML integration with microservices, automation advances, predictions for next-generation microservices, industry evolution, and best practice maturation. [^207]

### Concept-by-Concept Breakdown
#### **Gil** *(p.304)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.304, lines 22–29)*:
```
costs, but is a general metric that has been scientifically proven by Forsgren et al. to
be a powerful indicator of team agility. When applied to independently deployable
microservices, in our experience it can also indicate the health of a microservices
transformation trajectory.
By consistently measuring the three metrics and ensuring the transformation is on
the right track, teams can free themselves from the anxiety of achieving perfection in
every single microservices trait, freeing themselves for long-term success.
Summary
```
[^208]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.307)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.307, lines 34–41)*:
```
feedback, 53
overabstraction, 37
product-oriented perspective, 37, 39
Reservations API, 45
versus microservices, 54-56
architecture, 3
(see also microservices)
change and, 266
```
[^209]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.303)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.303, lines 4–11)*:
```
structure setup, tech stack upgrades, and experimentation with cool new tools, criti‐
cally delaying delivery of business value. Such delays can easily lead to stakeholders
shutting down a transformation effort before it even gets properly started.
It is extremely important to remember that microservices architec‐
ture is a journey, not just a destination. In this journey, the trajec‐
tory of the progress means everything, and surprising as it may
sound, current state is of much less significance. This is especially
true in the early days of the transformation efforts.
```
[^210]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 21 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.304)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.304, lines 32–39)*:
```
bullet” and it is important to understand that the final effect is achieved by shifting
complexity, not necessarily magically eliminating it. When we make such assertions,
it also helps to be clear what we mean by “complexity,” and it is different from the
notion of “complicated” systems, and what role “easy” versus “simple” architectural
approaches play in classifying various system delivery approaches.
We then shared our perspective on the importance of patience and a long-term out‐
look during a microservices transformation. It is a journey and a marathon, not a
288 
```
[^211]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.304)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.304, lines 32–39)*:
```
bullet” and it is important to understand that the final effect is achieved by shifting
complexity, not necessarily magically eliminating it. When we make such assertions,
it also helps to be clear what we mean by “complexity,” and it is different from the
notion of “complicated” systems, and what role “easy” versus “simple” architectural
approaches play in classifying various system delivery approaches.
We then shared our perspective on the importance of patience and a long-term out‐
look during a microservices transformation. It is a journey and a marathon, not a
288 
```
[^212]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.307)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.307, lines 62–69)*:
```
asset publishing, 131-132
asynchronous integration, DDD (domain-
driven design), 65
atomicity (ACID), 82
automated testing, workspace, 184
AWS (Amazon Web Services)
APIs, Terraform and, 110
ARN (Amazon Resource Name), 114
```
[^213]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.304)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.304, lines 35–41)*:
```
notion of “complicated” systems, and what role “easy” versus “simple” architectural
approaches play in classifying various system delivery approaches.
We then shared our perspective on the importance of patience and a long-term out‐
look during a microservices transformation. It is a journey and a marathon, not a
288 
| 
Chapter 12: A Journey’s End (and a New Beginning)
```
[^214]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.303)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.303, lines 22–29)*:
```
nation cost” as a value. Some teams try measuring “speed” or “safety,” but that is
equally problematic, as these values are derivatives and measurements are indefensi‐
ble. You will almost certainly notice a perceived increase in speed and safety, but to
claim causality, what are you going to compare the new speed to? Nobody builds the
same exact system once as a monolith and then as a microservices architecture. Any
increase in speed will be intuitively rewarding but unscientific. The same idea applies
to attempts of measuring increases in safety as well.
Instead, we propose measuring three values, two of which are directly related to the
```
[^215]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Encapsulation** *(p.311)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.311, lines 32–39)*:
```
HCL
encapsulation, 120
fmt command, 122
JSON and, 119
sandbox repository, 120
Terraform and, 119
validation, 122
health checks, 218-220
```
[^216]
**Annotation:** This excerpt demonstrates 'encapsulation' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.316)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.316, lines 17–24)*:
```
data element, 151
files, applying, 130
HCL and, 119-120
installation, 105
JSON-based state file, 115
modules, 142-145
AWS provider, 147
local variables, 147
```
[^217]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **From** *(p.318)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.318, lines 18–25)*:
```
Sparkling violetears are iridescent green with purple markings on the head and chest.
The longer purple feathers at their ears extend outward from their heads during dis‐
play. Large for hummingbirds, they average about five to six inches long, and weigh
about a quarter ounce. Females lay two eggs in a nest of their own making, and incu‐
bate the eggs. The chicks fledge from the nest at three weeks.
Because they live at higher, colder altitudes, sparkling violetears are among the spe‐
cies of hummingbirds that enter a deep torpor each night to sleep. In this
hibernation-like state of reduced body functions and a near-acclimation to surround‐
```
[^218]
**Annotation:** This excerpt demonstrates 'from' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Function** *(p.315)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.315, lines 8–15)*:
```
Kubernetes
built-in functions, 240
MySQL, 240
repositories, 235
setup, 243
security
collaboration and, 23
EKS (Elastic Kubernetes Service), 162, 164
```
[^219]
**Annotation:** This excerpt demonstrates 'function' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Immutable** *(p.311)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.311, lines 64–71)*:
```
IBM MQ, 81
immutable infrastructure (DevOps), 99-100
IaC (infrastructure as code) and, 101
implementation cost
data changes, 277
infrastructure cost and, 270
microservice change, 273-274
independent deployability, 76
```
[^220]
**Annotation:** This excerpt demonstrates 'immutable' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Import** *(p.304)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.304, lines 14–21)*:
```
Tracking the number of dependencies that a team needs to clear before a code release
to production is also a quantity worth measuring. Another important example of the
type of event to track is whether teams need to often wait for other teams to make
code changes, caused by the change in a shared data model. The triggers and duration
of stoppages will vary depending on an organization and the business contexts. It’s
important to track both trigger types as well as stoppage duration, so that meaningful,
actionable lessons learned can be derived and improvements can be made.
The third metric, deployment frequency, does not directly measure coordination
```
[^221]
**Annotation:** This excerpt demonstrates 'import' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Instance** *(p.304)*

**Verbatim Educational Excerpt** *(Microservices Up and Running, p.304, lines 2–9)*:
```
see a gradual decrease in the size of autonomous teams and an increase in the amount
of time that teams can work independently. For instance, you may observe that aver‐
age autonomous team size in your organization used to be 15 to 20 members and
after implementing microservices it starts to gradually decrease to 10, 8, 6…
Likewise, you should observe a decrease in frequency of coordination-related dead‐
locks. A coordination deadlock is a stoppage during which an autonomous team is
waiting on another team for a shared capability to be made available for them; e.g., an
infrastructure team provisioning a highly available Kafka or Cassandra cluster, or a
```
[^222]
**Annotation:** This excerpt demonstrates 'instance' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---


---

### **Footnotes**

[^1]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 1, lines 1–25).
[^2]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 18, lines 1–8).
[^3]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 20, lines 2–9).
[^4]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 8, lines 22–29).
[^5]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 18, lines 30–37).
[^6]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 13, lines 3–10).
[^7]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 13, lines 23–28).
[^8]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 19, lines 4–11).
[^9]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 14, lines 19–26).
[^10]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 16, lines 30–35).
[^11]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 15, lines 11–18).
[^12]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 14, lines 22–29).
[^13]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 5, lines 4–8).
[^14]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 9, lines 8–15).
[^15]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 18, lines 4–11).
[^16]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 19, lines 1–8).
[^17]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 21, lines 1–1).
[^18]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 39, lines 1–1).
[^19]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 65, lines 1–1).
[^20]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 21, lines 1–25).
[^21]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 22, lines 1–8).
[^22]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 23, lines 2–9).
[^23]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 32, lines 27–34).
[^24]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 33, lines 1–8).
[^25]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 23, lines 28–35).
[^26]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 31, lines 11–18).
[^27]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 27, lines 4–11).
[^28]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 25, lines 29–36).
[^29]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 32, lines 4–11).
[^30]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 34, lines 28–35).
[^31]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 32, lines 1–8).
[^32]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 23, lines 22–29).
[^33]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 27, lines 13–20).
[^34]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 36, lines 5–12).
[^35]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 27, lines 26–31).
[^36]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 39, lines 1–1).
[^37]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 65, lines 1–1).
[^38]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 97, lines 1–1).
[^39]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 39, lines 1–25).
[^40]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 57, lines 25–32).
[^41]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 60, lines 9–16).
[^42]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 53, lines 35–42).
[^43]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 53, lines 1–8).
[^44]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 43, lines 9–16).
[^45]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 39, lines 9–16).
[^46]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 61, lines 19–24).
[^47]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 56, lines 2–9).
[^48]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 51, lines 4–11).
[^49]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 56, lines 30–37).
[^50]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 42, lines 2–9).
[^51]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 41, lines 16–23).
[^52]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 56, lines 1–8).
[^53]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 49, lines 11–18).
[^54]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 42, lines 30–36).
[^55]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 65, lines 1–1).
[^56]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 97, lines 1–1).
[^57]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 135, lines 1–1).
[^58]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 65, lines 1–25).
[^59]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 92, lines 14–21).
[^60]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 81, lines 19–26).
[^61]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 66, lines 33–40).
[^62]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 94, lines 4–11).
[^63]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 76, lines 38–42).
[^64]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 76, lines 38–42).
[^65]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 81, lines 17–24).
[^66]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 77, lines 28–34).
[^67]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 80, lines 7–14).
[^68]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 77, lines 20–27).
[^69]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 73, lines 16–23).
[^70]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 77, lines 7–14).
[^71]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 65, lines 16–23).
[^72]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 76, lines 10–17).
[^73]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 74, lines 27–34).
[^74]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 97, lines 1–1).
[^75]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 135, lines 1–1).
[^76]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 179, lines 1–1).
[^77]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 97, lines 1–25).
[^78]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 98, lines 10–17).
[^79]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 116, lines 1–8).
[^80]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 102, lines 8–15).
[^81]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 107, lines 23–30).
[^82]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 117, lines 1–8).
[^83]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 101, lines 4–11).
[^84]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 104, lines 17–24).
[^85]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 131, lines 6–13).
[^86]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 112, lines 4–10).
[^87]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 111, lines 3–10).
[^88]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 106, lines 8–15).
[^89]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 106, lines 26–33).
[^90]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 105, lines 17–24).
[^91]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 115, lines 16–23).
[^92]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 115, lines 2–9).
[^93]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 135, lines 1–1).
[^94]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 179, lines 1–1).
[^95]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 209, lines 1–1).
[^96]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 135, lines 1–25).
[^97]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 153, lines 1–8).
[^98]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 172, lines 1–8).
[^99]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 153, lines 9–16).
[^100]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 164, lines 3–10).
[^101]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 172, lines 32–39).
[^102]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 164, lines 1–8).
[^103]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 143, lines 35–39).
[^104]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 147, lines 5–12).
[^105]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 137, lines 20–27).
[^106]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 147, lines 1–8).
[^107]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 136, lines 7–14).
[^108]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 174, lines 33–40).
[^109]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 151, lines 6–13).
[^110]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 161, lines 1–8).
[^111]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 158, lines 10–17).
[^112]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 179, lines 1–1).
[^113]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 209, lines 1–1).
[^114]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 243, lines 1–1).
[^115]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 179, lines 1–25).
[^116]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 204, lines 32–39).
[^117]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 192, lines 14–21).
[^118]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 188, lines 11–18).
[^119]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 204, lines 1–8).
[^120]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 203, lines 22–29).
[^121]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 187, lines 17–24).
[^122]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 180, lines 1–8).
[^123]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 197, lines 13–20).
[^124]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 197, lines 31–38).
[^125]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 195, lines 13–20).
[^126]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 195, lines 13–20).
[^127]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 183, lines 1–8).
[^128]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 194, lines 20–27).
[^129]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 183, lines 35–42).
[^130]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 196, lines 17–24).
[^131]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 209, lines 1–1).
[^132]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 243, lines 1–1).
[^133]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 267, lines 1–1).
[^134]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 209, lines 1–25).
[^135]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 238, lines 38–45).
[^136]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 240, lines 31–38).
[^137]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 235, lines 6–13).
[^138]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 220, lines 15–22).
[^139]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 209, lines 1–8).
[^140]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 235, lines 18–25).
[^141]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 235, lines 20–27).
[^142]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 221, lines 17–24).
[^143]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 241, lines 33–40).
[^144]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 210, lines 15–22).
[^145]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 217, lines 29–34).
[^146]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 227, lines 14–21).
[^147]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 229, lines 8–15).
[^148]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 240, lines 25–32).
[^149]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 238, lines 18–25).
[^150]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 243, lines 1–1).
[^151]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 267, lines 1–1).
[^152]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 283, lines 1–1).
[^153]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 243, lines 1–25).
[^154]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 250, lines 1–8).
[^155]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 250, lines 24–31).
[^156]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 264, lines 5–12).
[^157]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 251, lines 3–10).
[^158]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 253, lines 1–8).
[^159]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 250, lines 28–35).
[^160]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 251, lines 19–26).
[^161]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 256, lines 23–30).
[^162]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 249, lines 1–8).
[^163]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 264, lines 28–35).
[^164]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 250, lines 14–21).
[^165]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 243, lines 4–11).
[^166]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 256, lines 10–17).
[^167]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 245, lines 5–12).
[^168]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 250, lines 1–8).
[^169]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 267, lines 1–1).
[^170]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 283, lines 1–1).
[^171]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 303, lines 1–1).
[^172]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 267, lines 1–25).
[^173]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 270, lines 2–9).
[^174]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 280, lines 3–10).
[^175]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 282, lines 15–22).
[^176]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 270, lines 3–10).
[^177]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 268, lines 35–42).
[^178]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 269, lines 5–12).
[^179]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 269, lines 32–37).
[^180]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 272, lines 1–8).
[^181]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 280, lines 3–10).
[^182]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 271, lines 19–26).
[^183]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 276, lines 4–11).
[^184]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 273, lines 41–46).
[^185]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 279, lines 7–14).
[^186]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 282, lines 14–21).
[^187]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 273, lines 36–43).
[^188]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 283, lines 1–1).
[^189]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 303, lines 1–1).
[^190]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 283, lines 1–25).
[^191]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 286, lines 1–8).
[^192]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 298, lines 1–8).
[^193]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 284, lines 10–17).
[^194]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 300, lines 1–8).
[^195]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 285, lines 1–8).
[^196]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 289, lines 30–35).
[^197]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 283, lines 13–20).
[^198]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 299, lines 31–38).
[^199]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 295, lines 28–35).
[^200]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 286, lines 20–27).
[^201]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 299, lines 1–8).
[^202]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 284, lines 1–8).
[^203]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 294, lines 15–22).
[^204]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 286, lines 4–11).
[^205]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 301, lines 16–23).
[^206]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 303, lines 1–1).
[^207]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 303, lines 1–25).
[^208]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 304, lines 22–29).
[^209]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 307, lines 34–41).
[^210]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 303, lines 4–11).
[^211]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 304, lines 32–39).
[^212]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 304, lines 32–39).
[^213]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 307, lines 62–69).
[^214]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 304, lines 35–41).
[^215]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 303, lines 22–29).
[^216]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 311, lines 32–39).
[^217]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 316, lines 17–24).
[^218]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 318, lines 18–25).
[^219]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 315, lines 8–15).
[^220]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 311, lines 64–71).
[^221]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 304, lines 14–21).
[^222]: Mitra, Ronnie and Nadareishvili, Irakli. *Microservices Up and Running*. (JSON `Microservices Up and Running.json`, p. 304, lines 2–9).
