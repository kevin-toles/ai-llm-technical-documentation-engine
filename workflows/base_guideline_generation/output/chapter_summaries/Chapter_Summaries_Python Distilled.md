# Comprehensive Python Guidelines — Python Distilled (Chapters 1-9)

*Source: Python Distilled, Chapters 1-9*

---

## Chapter 1: Python Basics

*Source: Python Distilled, pages 1–40*

### Chapter Summary
Introduces Python's fundamental building blocks including variables, basic data types (integers, floats, strings), and core data structures (lists, dictionaries, tuples, sets). Covers basic syntax, expressions, and statements. [^1]

### Concept-by-Concept Breakdown
#### **None** *(p.8)*

**Verbatim Educational Excerpt** *(Python Distilled, p.8, lines 25–32)*:
```
4.7
Using None for Optional or Missing
Data
87
4.8
Object Protocols and Data
Abstraction
87
```
[^2]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.17)*

**Verbatim Educational Excerpt** *(Python Distilled, p.17, lines 33–38)*:
```
print('Hello World')
Python source files are UTF-8-encoded text files that normally have a .py suffix. The
# character denotes a comment that extends to the end of the line. International (Unicode)
characters can be freely used in the source code as long as you use the UTF-8 encoding
(this is the default in most editors, but it never hurts to check your editor settings if you’re
unsure).
```
[^3]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.8)*

**Verbatim Educational Excerpt** *(Python Distilled, p.8, lines 30–37)*:
```
Object Protocols and Data
Abstraction
87
4.9
Object Protocol
89
4.10
Number Protocol
```
[^4]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Annotation** *(p.38)*

**Verbatim Educational Excerpt** *(Python Distilled, p.38, lines 16–23)*:
```
return r
Such annotations are merely informational and are not actually enforced at runtime.
Someone could still call the above function with non-integer values, such as result =
remainder(37.5, 3.2).
Use a tuple to return multiple values from a function:
def divide(a, b):
q = a // b
# If a and b are integers, q is integer
```
[^5]
**Annotation:** This excerpt demonstrates 'annotation' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.8)*

**Verbatim Educational Excerpt** *(Python Distilled, p.8, lines 67–74)*:
```
5.2
Default Arguments 101
5.3
Variadic Arguments 102
5.4
Keyword Arguments 103
5.5
Variadic Keyword Arguments 104
```
[^6]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.31)*

**Verbatim Educational Excerpt** *(Python Distilled, p.31, lines 32–39)*:
```
portfolio.append(holding)
The resulting portfolio list created by this program looks like a two-dimensional array
of rows and columns. Each row is represented by a tuple and can be accessed as follows:
>>> portfolio[0]
('AA', 100, 32.2)
>>> portfolio[1]
('IBM', 50, 91.1)
>>>
```
[^7]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.40)*

**Verbatim Educational Excerpt** *(Python Distilled, p.40, lines 3–10)*:
```
print('Bad row:', row)
print('Reason:', err)
In this code, if a ValueError occurs, details concerning the cause of the error are placed
in err and control passes to the code in the except block. If some other kind of exception
is raised, the program crashes as usual. If no errors occur, the code in the except block is
ignored. When an exception is handled, program execution resumes with the statement
that immediately follows the last except block. The program does not return to the
location where the exception occurred.
```
[^8]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 14 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.7)*

**Verbatim Educational Excerpt** *(Python Distilled, p.7, lines 90–95)*:
```
3.6
Assertions and __debug__
77
3.7
Final Words
78
```
[^9]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.7)*

**Verbatim Educational Excerpt** *(Python Distilled, p.7, lines 90–95)*:
```
3.6
Assertions and __debug__
77
3.7
Final Words
78
```
[^10]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.12)*

**Verbatim Educational Excerpt** *(Python Distilled, p.12, lines 25–32)*:
```
Concurrent Execution with
asyncio 272
9.15
Standard Library Modules 273
9.15.1
asyncio Module 273
9.15.2
binascii Module 274
```
[^11]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.12)*

**Verbatim Educational Excerpt** *(Python Distilled, p.12, lines 25–32)*:
```
Concurrent Execution with
asyncio 272
9.15
Standard Library Modules 273
9.15.1
asyncio Module 273
9.15.2
binascii Module 274
```
[^12]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.9)*

**Verbatim Educational Excerpt** *(Python Distilled, p.9, lines 17–24)*:
```
5.20
Function Introspection, Attributes,
and Signatures 129
5.21
Environment Inspection 131
5.22
Dynamic Code Execution and
Creation 133
```
[^13]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.9)*

**Verbatim Educational Excerpt** *(Python Distilled, p.9, lines 26–33)*:
```
Asynchronous Functions and
await 135
5.24
Final Words: Thoughts on Functions
and Composition 137
6
Generators 139
6.1
```
[^14]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.21)*

**Verbatim Educational Excerpt** *(Python Distilled, p.21, lines 50–56)*:
```
Less than or equal to
The result of a comparison is a Boolean value True or False.
The and, or, and not operators (not to be confused with the bit-manipulation
operators above) can form more complex Boolean expressions. The behavior of these
operators is as shown in Table 1.5.
A value is considered false if it is literally False, None, numerically zero, or empty.
Otherwise, it’s considered true.
```
[^15]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.27)*

**Verbatim Educational Excerpt** *(Python Distilled, p.27, lines 31–38)*:
```
The := operator used in this example assigns to a variable and returns its value so that it
can be tested by the while loop to break out. When the end of a file is reached, read()
returns an empty string. An alternate way to write the above function is using break:
with open('data.txt') as file:
while True:
chunk = file.read(10000)
if not chunk:
break
```
[^16]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 2: Operators, Expressions, and Data Manipulation** *(pp.41–62)*

This later chapter builds upon the concepts introduced here, particularly: None, argument, array.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^17]

**Annotation:** Forward reference: Chapter 2 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, argument appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 3: Program Structure and Control Flow** *(pp.63–88)*

This later chapter builds upon the concepts introduced here, particularly: None, argument, array.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^18]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, argument appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Objects, Types, and Protocols** *(pp.89–124)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, abstraction.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^19]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 2: Operators, Expressions, and Data Manipulation

*Source: Python Distilled, pages 41–62*

### Chapter Summary
Explores Python's operator system including arithmetic, comparison, logical, and bitwise operators. Covers expression evaluation, operator precedence, slicing, indexing, and various data manipulation techniques. [^20]

### Concept-by-Concept Breakdown
#### **None** *(p.59)*

**Verbatim Educational Excerpt** *(Python Distilled, p.59, lines 5–12)*:
```
example, consider this function:
def f(x, items=None):
if not items:
items = []
items.append(x)
return items
This function has an optional argument that, if not given, causes a new list to be created
and returned. For example,
```
[^21]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.42)*

**Verbatim Educational Excerpt** *(Python Distilled, p.42, lines 12–19)*:
```
class Stack:
def __init__(self):
# Initialize the stack
self._items = [ ]
def push(self, item):
self._items.append(item)
def pop(self):
return self._items.pop()
```
[^22]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.48)*

**Verbatim Educational Excerpt** *(Python Distilled, p.48, lines 2–9)*:
```
33
if __name__ == '__main__':
main()
__name__ is a built-in variable that always contains the name of the enclosing module.
If a program is run as the main script with a command such as python readport.py,
the __name__ variable is set to '__main__'. Otherwise, if the code is imported using a
statement such as import readport, the __name__ variable is set to 'readport'.
As shown, the program is hardcoded to use a filename 'portfolio.csv'. Instead, you
```
[^23]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.48)*

**Verbatim Educational Excerpt** *(Python Distilled, p.48, lines 2–9)*:
```
33
if __name__ == '__main__':
main()
__name__ is a built-in variable that always contains the name of the enclosing module.
If a program is run as the main script with a command such as python readport.py,
the __name__ variable is set to '__main__'. Otherwise, if the code is imported using a
statement such as import readport, the __name__ variable is set to 'readport'.
As shown, the program is hardcoded to use a filename 'portfolio.csv'. Instead, you
```
[^24]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Repr__** *(p.43)*

**Verbatim Educational Excerpt** *(Python Distilled, p.43, lines 7–14)*:
```
to answer to your coworkers when they review your code.
The __repr__() and __len__() methods are there to make the object play nicely with
the rest of the environment. Here, __len__() makes a Stack work with the built-in len()
function and __repr__() changes the way that a Stack is displayed and printed. It’s a good
idea to always define __repr__() as it can simplify debugging.
>>> s = Stack()
>>> s.push('Dave')
>>> s.push(42)
```
[^25]
**Annotation:** This excerpt demonstrates '__repr__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argparse** *(p.48)*

**Verbatim Educational Excerpt** *(Python Distilled, p.48, lines 35–41)*:
```
For very simple programs, it is often enough to process arguments in sys.argv as
shown. For more advanced usage, the argparse standard library module can be used.
1.19
Packages
In large programs, it’s common to organize code into packages. A package is a hierarchical
collection of modules. On the filesystem, put your code as a collection of files in a
directory like this:
```
[^26]
**Annotation:** This excerpt demonstrates 'argparse' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.59)*

**Verbatim Educational Excerpt** *(Python Distilled, p.59, lines 10–17)*:
```
return items
This function has an optional argument that, if not given, causes a new list to be created
and returned. For example,
>>> foo(4)
[4]
>>>
However, the function has really strange behavior if you give it an existing empty list as
an argument:
```
[^27]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.51)*

**Verbatim Educational Excerpt** *(Python Distilled, p.51, lines 34–40)*:
```
of Python is a small programming language along with a useful collection of built-in
objects—lists, sets, and dictionaries. A vast array of practical problems can be solved using
nothing more than the basic features presented in this chapter. This is a good thing to
keep in mind as you begin your Python adventure—although there are always more
complicated ways to solve a problem, there might also be a simple way to do it with the
basic features Python already provides. When in doubt, you’ll probably thank your past self
for doing just that.
```
[^28]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.53)*

**Verbatim Educational Excerpt** *(Python Distilled, p.53, lines 3–10)*:
```
Operators, Expressions, and Data Manipulation
Internally, floating-point numbers are stored as IEEE 754 double-precision (64-bit)
values.
In numeric literals, a single underscore ( _ ) can be used as a visual separator between
digits. For example:
123_456_789
0x1234_5678
0b111_00_101
```
[^29]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 15 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.42)*

**Verbatim Educational Excerpt** *(Python Distilled, p.42, lines 25–32)*:
```
argument in each method always refers to the object itself. By convention, self is the
name used for this argument. All operations involving the attributes of an object must
explicitly refer to the self variable.
Methods with leading and trailing double underscores are special methods. For
example, __init__ is used to initialize an object. In this case, __init__ creates an internal
list for storing the stack data.
To use a class, write code such as this:
s = Stack()
```
[^30]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.58)*

**Verbatim Educational Excerpt** *(Python Distilled, p.58, lines 1–8)*:
```
2.7 Boolean Expressions and Truth Values
43
For sets, x < y tests if x is strict subset of y (i.e., has fewer elements, but is not equal
to y).
When comparing two sequences, the first elements of each sequence are compared. If
they differ, this determines the result. If they’re the same, the comparison moves to the
second element of each sequence. This process continues until two different elements are
found or no more elements exist in either of the sequences. If the end of both sequences is
```
[^31]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.51)*

**Verbatim Educational Excerpt** *(Python Distilled, p.51, lines 18–25)*:
```
To make a sandbox where you can install packages and work without worrying about
breaking anything, create a virtual environment by a command like this:
bash % python3 -m venv myproject
This will set up a dedicated Python installation for you in a directory called
myproject/. Within that directory, you’ll find an interpreter executable and library where
you can safely install packages. For example, if you run myproject/bin/python3, you’ll
get an interpreter configured for your personal use. You can install packages into this
interpreter without worrying about breaking any part of the default Python installation.
```
[^32]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.42)*

**Verbatim Educational Excerpt** *(Python Distilled, p.42, lines 1–8)*:
```
1.16 Objects and Classes
27
double underscore. These methods implement various operators. For example, the
__add__() method is used to implement the + operator. These methods are explained in
more detail in later chapters.
>>> items.__add__([73, 101])
[37, 42, 73, 101]
>>>
```
[^33]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.41)*

**Verbatim Educational Excerpt** *(Python Distilled, p.41, lines 13–20)*:
```
On exit, the interpreter makes a best effort to garbage-collect all active objects.
However, if you need to perform a specific cleanup action (remove files, close a
connection), you can register it with the atexit module as follows:
import atexit
# Example
connection = open_connection("deaddot.com")
def cleanup():
print "Going away..."
```
[^34]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Continue** *(p.50)*

**Verbatim Educational Excerpt** *(Python Distilled, p.50, lines 2–9)*:
```
35
Managing all of this is a complex topic that continues to evolve. There are also many
conflicting opinions about what constitutes “best practice.” However, there are a few
essential facets to it that you should know.
First, it is standard practice to organize large code bases into packages (that is,
directories of .py files that include the special __init__.py file). When doing this, pick
a unique package name for the top-level directory name. The primary purpose of the
package directory is to manage import statements and the namespaces of modules used
```
[^35]
**Annotation:** This excerpt demonstrates 'continue' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 3: Program Structure and Control Flow** *(pp.63–88)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^36]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Objects, Types, and Protocols** *(pp.89–124)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^37]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Functions** *(pp.125–162)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^38]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 3: Program Structure and Control Flow

*Source: Python Distilled, pages 63–88*

### Chapter Summary
Details Python's control flow mechanisms including conditionals (if/elif/else), loops (while/for), and flow control statements (break, continue, pass). Emphasizes proper indentation and statement blocks. [^39]

### Concept-by-Concept Breakdown
#### **None** *(p.69)*

**Verbatim Educational Excerpt** *(Python Distilled, p.69, lines 12–19)*:
```
except ValueError:
return None
values = [ '1', '2', '-4', 'n/a', '-3', '5' ]
data1 = [ toint(x) for x in values ]
# data1 = [1, 2, -4, None, -3, 5]
data2 = [ toint(x) for x in values if toint(x) is not None ]
# data2 = [1, 2, -4, -3, 5]
The double evaluation of toint(x) in the last example can be avoided by using the :=
```
[^40]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.85)*

**Verbatim Educational Excerpt** *(Python Distilled, p.85, lines 3–10)*:
```
Program Structure and Control Flow
When you create a custom exception class that redefines __init__(), it is important to
assign a tuple containing the arguments of __init__() to the attribute self.args as
shown. This attribute is used when printing exception traceback messages. If you leave it
undefined, users won’t be able to see any useful information about the exception when an
error occurs.
Exceptions can be organized into a hierarchy using inheritance. For instance, the
NetworkError exception defined earlier could serve as a base class for a variety of more
```
[^41]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.86)*

**Verbatim Educational Excerpt** *(Python Distilled, p.86, lines 18–25)*:
```
raise ApplicationError('It failed') from e
__main__.ApplicationError: It failed
>>>
If you catch an ApplicationError, the __cause__ attribute of the resulting exception
will contain the other exception. For example:
try:
spam()
except ApplicationError as e:
```
[^42]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.71)*

**Verbatim Educational Excerpt** *(Python Distilled, p.71, lines 22–29)*:
```
The Function Call () Operator
The f(args) operator is used to make a function call on f. Each argument to a function
is an expression. Prior to calling the function, all of the argument expressions are fully
evaluated from left to right. This is known as applicative order evaluation. More
information about functions can be found in Chapter 5.
2.18
Order of Evaluation
Table 2.11 lists the order of operation (precedence rules) for Python operators. All
```
[^43]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.71)*

**Verbatim Educational Excerpt** *(Python Distilled, p.71, lines 3–10)*:
```
Operators, Expressions, and Data Manipulation
When passed as a single function argument, one set of parentheses can be removed. For
example, the following statements are equivalent:
sum((x*x for x in values))
sum(x*x for x in values)
# Extra parens removed
In both cases, a generator (x*x for x in values) is created and passed to the sum()
function.
```
[^44]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.73)*

**Verbatim Educational Excerpt** *(Python Distilled, p.73, lines 16–23)*:
```
records returned by a query. Chances are, you will use the for statement to do just that.
Or, suppose you’re working with numeric arrays and want to perform element-by-element
mathematics on arrays. You might think that the standard math operators would work—
and your intuition would be correct. Or, suppose you’re using a library to fetch data over
HTTP and you want to access the contents of the HTTP headers. There’s a good chance
that data will be presented in a way that looks like a dictionary.
More information about Python’s internal protocols and how to customize them is
given in Chapter 4.
```
[^45]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.83)*

**Verbatim Educational Excerpt** *(Python Distilled, p.83, lines 5–12)*:
```
Exception Categories
Exception Class
Description
BaseException
The root class for all exceptions
Exception
Base class for all program-related errors
ArithmeticError
```
[^46]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 24 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.83)*

**Verbatim Educational Excerpt** *(Python Distilled, p.83, lines 30–37)*:
```
Description
AssertionError
Failed assert statement
AttributeError
Bad attribute lookup on an object
EOFError
End of file
MemoryError
```
[^47]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.83)*

**Verbatim Educational Excerpt** *(Python Distilled, p.83, lines 30–37)*:
```
Description
AssertionError
Failed assert statement
AttributeError
Bad attribute lookup on an object
EOFError
End of file
MemoryError
```
[^48]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.84)*

**Verbatim Educational Excerpt** *(Python Distilled, p.84, lines 12–19)*:
```
(typically by pressing Control-C in a terminal). This exception is a bit unusual in that it is
asynchronous—meaning that it could occur at almost any time and on any statement in
your program. The default behavior of Python is to simply terminate when this happens.
If you want to control the delivery of SIGINT, the signal library module can be used (see
Chapter 9).
The StopIteration exception is part of the iteration protocol and signals the end of
iteration.
3.4.3
```
[^49]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.88)*

**Verbatim Educational Excerpt** *(Python Distilled, p.88, lines 6–13)*:
```
The difference between these two cases is subtle but important. That is why exception
chaining information is placed into either the __cause__ or the __context__ attribute.
The __cause__ attribute is reserved for when you’re expecting the possibility of a failure.
The __context__ attribute is set in both cases, but would be the only source of
information for an unexpected exception raised while handling another exception.
3.4.5
Exception Tracebacks
Exceptions have an associated stack traceback that provides information about where an
```
[^50]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.73)*

**Verbatim Educational Excerpt** *(Python Distilled, p.73, lines 6–13)*:
```
be customized so the bitwise operators are used instead—even though they have a higher
precedence level and evaluate differently when used in Boolean relations.
2.19
Final Words: The Secret Life of Data
One of the most frequent uses of Python is in applications involving data manipulation and
analysis. Here, Python provides a kind of “domain language” for thinking about your
problem. The built-in operators and expressions are at the core of that language and
everything else builds from it. Thus, once you build a kind of intuition around Python’s
```
[^51]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.78)*

**Verbatim Educational Excerpt** *(Python Distilled, p.78, lines 10–17)*:
```
...
The break and continue statements apply only to the innermost loop being executed.
If you need to break out of a deeply nested loop structure, you can use an exception.
Python doesn’t provide a “goto” statement. You can also attach the else statement to loop
constructs, as in the following example:
# for-else
with open('foo.txt') as file:
for line in file:
```
[^52]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.83)*

**Verbatim Educational Excerpt** *(Python Distilled, p.83, lines 5–12)*:
```
Exception Categories
Exception Class
Description
BaseException
The root class for all exceptions
Exception
Base class for all program-related errors
ArithmeticError
```
[^53]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 11 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.81)*

**Verbatim Educational Excerpt** *(Python Distilled, p.81, lines 26–33)*:
```
data = file.read()
file.close()
The finally statement defines a cleanup action that must execute regardless of what
happens in a try-except block. Here’s an example:
file = open('foo.txt', 'rt')
try:
# Do some stuff
...
```
[^54]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 4: Objects, Types, and Protocols** *(pp.89–124)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, args.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^55]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Functions** *(pp.125–162)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, args.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^56]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Generators** *(pp.163–182)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^57]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 4: Objects, Types, and Protocols

*Source: Python Distilled, pages 89–124*

### Chapter Summary
Examines Python's object model, type system, and protocols. Covers special methods (magic methods), duck typing, polymorphism, and the distinction between mutable and immutable objects. [^58]

### Concept-by-Concept Breakdown
#### **None** *(p.102)*

**Verbatim Educational Excerpt** *(Python Distilled, p.102, lines 14–21)*:
```
4.7
Using None for Optional or
Missing Data
Sometimes programs need to represent an optional or missing value. None is a special
instance reserved for this purpose. None is returned by functions that don’t explicitly return
a value. None is also frequently used as the default value of optional arguments, so that the
function can detect whether the caller has actually passed a value for that argument. None
has no attributes and evaluates to False in Boolean expressions.
```
[^59]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 10 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.105)*

**Verbatim Educational Excerpt** *(Python Distilled, p.105, lines 13–20)*:
```
a = repr(f)
# a = "<_io.TextIOWrapper name='foo.txt' mode='r' encoding='UTF-8'>
4.10
Number Protocol
Table 4.2 lists special methods that objects must implement to provide mathematical
operations.
Table 4.2
Methods for Mathematical Operations
```
[^60]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.90)*

**Verbatim Educational Excerpt** *(Python Distilled, p.90, lines 30–37)*:
```
control flow enters and exits the associated block of statements that follow. When the with
obj statement executes, it calls the method obj.__enter__() to signal that a new context
is being entered. When control flow leaves the context, the method obj.__exit__(type,
value, traceback) executes. If no exception has been raised, the three arguments to
__exit__() are all set to None. Otherwise, they contain the type, value, and traceback
associated with the exception that has caused the control flow to leave the context. If the
__exit__() method returns True, it indicates that the raised exception was handled and
should no longer be propagated. Returning None or False will cause the exception to
```
[^61]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Eq__** *(p.108)*

**Verbatim Educational Excerpt** *(Python Distilled, p.108, lines 8–15)*:
```
Returns False or True for truth-value testing
__eq__(self, other)
self == other
__ne__(self, other)
self != other
__lt__(self, other)
self < other
__le__(self, other)
```
[^62]
**Annotation:** This excerpt demonstrates '__eq__' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.114)*

**Verbatim Educational Excerpt** *(Python Distilled, p.114, lines 17–24)*:
```
the with statement.
__exit__(self, type, value, tb)
Called when leaving a context. If an exception
occurred, type, value, and tb have the exception
type, value, and traceback information.
The __enter__() method is invoked when the with statement executes. The value
returned by this method is placed into the variable specified with the optional as var
specifier. The __exit__() method is called as soon as control flow leaves the block of
```
[^63]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.104)*

**Verbatim Educational Excerpt** *(Python Distilled, p.104, lines 16–23)*:
```
A static method called to create a new instance.
__init__(self [,*args [,**kwargs]])
Called to initialize a new instance after it’s been
created.
__del__(self)
Called when an instance is being destroyed.
__repr__(self)
Create a string representation.
```
[^64]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.121)*

**Verbatim Educational Excerpt** *(Python Distilled, p.121, lines 18–25)*:
```
function whatever you want as long as the name is a valid identifier.
The name of a function can be obtained via the __name__ attribute. This is sometimes
useful for debugging.
>>> def square(x):
...
return x * x
...
>>> square.__name__
```
[^65]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Repr__** *(p.104)*

**Verbatim Educational Excerpt** *(Python Distilled, p.104, lines 21–28)*:
```
Called when an instance is being destroyed.
__repr__(self)
Create a string representation.
The __new__() and __init__() methods are used together to create and initialize
instances. When an object is created by calling SomeClass(args), it is translated into the
following steps:
x = SomeClass.__new__(SomeClass, args)
if isinstance(x, SomeClass):
```
[^66]
**Annotation:** This excerpt demonstrates '__repr__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Str__** *(p.109)*

**Verbatim Educational Excerpt** *(Python Distilled, p.109, lines 27–34)*:
```
Description
__str__(self)
Conversion to a string
__bytes__(self)
Conversion to bytes
__format__(self, format_spec)
Creates a formatted representation
__bool__(self)
```
[^67]
**Annotation:** This excerpt demonstrates '__str__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.102)*

**Verbatim Educational Excerpt** *(Python Distilled, p.102, lines 1–8)*:
```
4.8 Object Protocols and Data Abstraction
87
_formats = {
'text': TextFormatter,
'csv': CSVFormatter,
'html': HTMLFormatter
}
if format in _formats:
```
[^68]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Annotation** *(p.122)*

**Verbatim Educational Excerpt** *(Python Distilled, p.122, lines 12–19)*:
```
presence of hints provides no performance benefits or extra runtime error checking. The
hints are merely stored in the __annotations__ attribute of the function which is a
dictionary mapping argument names to the supplied hints. Third-party tools such as IDEs
and code checkers might use the hints for various purposes.
Sometimes you will see type hints attached to local variables within a function. For
example:
def factorial(n:int) -> int:
result: int = 1
```
[^69]
**Annotation:** This excerpt demonstrates 'annotation' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.119)*

**Verbatim Educational Excerpt** *(Python Distilled, p.119, lines 34–41)*:
```
# Accept variable number of positional or keyword arguments
def func(*args, **kwargs):
# args is a tuple of positional args
# kwargs is dictionary of keyword args
...
This combined use of *args and **kwargs is commonly used to write wrappers,
decorators, proxies, and similar functions. For example, suppose you have a function to
parse lines of text taken from an iterable:
```
[^70]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.118)*

**Verbatim Educational Excerpt** *(Python Distilled, p.118, lines 1–8)*:
```
5.4 Keyword Arguments
103
5.4
Keyword Arguments
Function arguments can be supplied by explicitly naming each parameter and specifying a
value. These are known as keyword arguments. Here is an example:
def func(w, x, y, z):
statements
```
[^71]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 19 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.103)*

**Verbatim Educational Excerpt** *(Python Distilled, p.103, lines 15–22)*:
```
>>>
Not only that—the function works with arrays and other complex structures from
packages such as numpy. For example:
>>> import numpy as np
>>> prices = np.array([1.25, 2.10, 3.05])
>>> units = np.array([50, 20, 25])
>>> compute_cost(prices, quantities)
array([62.5 , 42.
```
[^72]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.90)*

**Verbatim Educational Excerpt** *(Python Distilled, p.90, lines 2–9)*:
```
75
crashes with some kind of ApplicationError defined above, you’ll know immediately
why that error got raised—because you wrote the code to do it. On the other hand, if
the program crashes with one of Python’s built-in exceptions (such as TypeError or
ValueError), that might indicate a more serious problem.
3.5
Context Managers and the with
Statement
```
[^73]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 19 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 5: Functions** *(pp.125–162)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^74]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Generators** *(pp.163–182)*

This later chapter builds upon the concepts introduced here, particularly: None, __enter__, __exit__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^75]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __enter__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Classes and Object-Oriented Programming** *(pp.183–228)*

This later chapter builds upon the concepts introduced here, particularly: None, __enter__, __exit__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^76]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __enter__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 5: Functions

*Source: Python Distilled, pages 125–162*

### Chapter Summary
Comprehensive coverage of Python functions including parameter passing, return values, lambda functions, closures, decorators, and scope rules. Discusses namespaces, global/nonlocal keywords, and various parameter types. [^77]

### Concept-by-Concept Breakdown
#### **None** *(p.125)*

**Verbatim Educational Excerpt** *(Python Distilled, p.125, lines 14–21)*:
```
One approach is to treat the result as optional—that is, the function either works by
returning an answer or returns None which is commonly used to indicate a missing value.
For example, the function could be modified like this:
def parse_value(text):
parts = text.split('=', 1)
if len(parts) == 2:
return ParseResult(parts[0].strip(), parts[1].strip())
else:
```
[^78]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.149)*

**Verbatim Educational Excerpt** *(Python Distilled, p.149, lines 26–33)*:
```
A common use of dynamic code execution is for creating functions and methods. For
example, here’s a function that creates an __init__() method for a class given a list of
names:
def make_init(*names):
parms = ','.join(names)
code = f'def __init__(self, {parms}):\n'
for name in names:
code += f'
```
[^79]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.141)*

**Verbatim Educational Excerpt** *(Python Distilled, p.141, lines 7–14)*:
```
# Create the decoration function
temp = trace("You called {func.__name__}")
# Apply it to func
func = temp(func)
In this case, the outermost function that accepts the arguments is responsible for creating
a decoration function. That function is then called with the function to be decorated to
obtain the final result. Here’s what the decorator implementation might look like:
from functools import wraps
```
[^80]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.160)*

**Verbatim Educational Excerpt** *(Python Distilled, p.160, lines 21–28)*:
```
hooked together into a workflow to solve a problem.
Making each component small and isolated is a good abstraction technique. For
example, consider the get_comments() generator. As input, it takes any iterable producing
lines of text. This text could come from almost anywhere—a file, a list, a generator, and so
on. As a result, this functionality is much more powerful and adaptable than it was when it
was embedded into a deeply nested for loop involving files. Generators thus encourage
code reuse by breaking problems into small well-defined computational tasks. Smaller tasks
are also easier to reason about, debug, and test.
```
[^81]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Annotation** *(p.144)*

**Verbatim Educational Excerpt** *(Python Distilled, p.144, lines 22–29)*:
```
Documentation string
f.__annotations__
Type hints
f.__globals__
Dictionary that is the global namespace
f.__closure__
Closure variables (if any)
f.__code__
```
[^82]
**Annotation:** This excerpt demonstrates 'annotation' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.136)*

**Verbatim Educational Excerpt** *(Python Distilled, p.136, lines 7–14)*:
```
might be to use positional-only arguments. For example:
def after(seconds, func, debug=False, /, *args, **kwargs):
time.sleep(seconds)
if debug:
print('About to call', func, args, kwargs)
func(*args, **kwargs)
after(10, add, 2, y=3)
Another possibly unsettling insight is that after() actually represents two different
```
[^83]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 14 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.135)*

**Verbatim Educational Excerpt** *(Python Distilled, p.135, lines 7–14)*:
```
As an aside, partial function application is closely related to a concept known as currying.
Currying is a functional programming technique where a multiple-argument function is
expressed as a chain of nested single-argument functions. Here is an example:
# Three-argument function
def f(x, y, z):
return x + y + z
# Curried version
def fc(x):
```
[^84]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 13 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.151)*

**Verbatim Educational Excerpt** *(Python Distilled, p.151, lines 3–10)*:
```
Functions
async def make_greeting(name):
return f'Hello {name}'
async def main():
for name in ['Paula', 'Thomas', 'Lewis']:
a = await make_greeting(name)
print(a)
# Run it.
```
[^85]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 27 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.146)*

**Verbatim Educational Excerpt** *(Python Distilled, p.146, lines 13–20)*:
```
pass
assert inspect.signature(func1) == inspect.signature(func2)
This kind of comparison might be useful in frameworks. For example, a framework
could use signature comparison to see if you’re writing functions or methods that conform
to an expected prototype.
If stored in the __signature__ attribute of a function, a signature will be shown in help
messages and returned on further uses of inspect.signature(). For example:
def func(x, y, z=None):
```
[^86]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.150)*

**Verbatim Educational Excerpt** *(Python Distilled, p.150, lines 1–8)*:
```
5.23 Asynchronous Functions and await
135
5.23
Asynchronous Functions and await
Python provides a number of language features related to the asynchronous execution of
code. These include so-called async functions (or coroutines) and awaitables. They are mostly
used by programs involving concurrency and the asyncio module. However, other
libraries may also build upon these.
```
[^87]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 21 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.150)*

**Verbatim Educational Excerpt** *(Python Distilled, p.150, lines 6–13)*:
```
code. These include so-called async functions (or coroutines) and awaitables. They are mostly
used by programs involving concurrency and the asyncio module. However, other
libraries may also build upon these.
An asynchronous function, or coroutine function, is defined by prefacing a normal
function definition with the extra keyword async. For example:
async def greeting(name):
print(f'Hello {name}')
If you call such a function, you’ll find that it doesn’t execute in the usual way—in fact,
```
[^88]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.144)*

**Verbatim Educational Excerpt** *(Python Distilled, p.144, lines 1–8)*:
```
5.20 Function Introspection, Attributes, and Signatures
129
5.20
Function Introspection, Attributes,
and Signatures
As you have seen, functions are objects—which means they can be assigned to variables,
placed in data structures, and used in the same way as any other kind of data in a program.
They can also be inspected in various ways. Table 5.1 shows some common attributes of
```
[^89]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 10 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.151)*

**Verbatim Educational Excerpt** *(Python Distilled, p.151, lines 7–14)*:
```
for name in ['Paula', 'Thomas', 'Lewis']:
a = await make_greeting(name)
print(a)
# Run it.
Will see greetings for Paula, Thomas, and Lewis
asyncio.run(main())
Use of await is only valid within an enclosing async function definition. It’s also a
required part of making async functions execute. If you leave off the await, you’ll find that
```
[^90]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.156)*

**Verbatim Educational Excerpt** *(Python Distilled, p.156, lines 16–23)*:
```
if n == 2:
break
statements
In this example, the for loop aborts by calling break and the associated generator never
runs to full completion. If it’s important for your generator function to perform some kind
of cleanup action, make sure you use try-finally or a context manager. For example:
def countdown(n):
print('Counting down from', n)
```
[^91]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Bytecode** *(p.145)*

**Verbatim Educational Excerpt** *(Python Distilled, p.145, lines 5–12)*:
```
>>>
The f.__code__ object represents the compiled interpreter bytecode for the
function body.
Functions can have arbitrary attributes attached to them. Here’s an example:
def func():
statements
func.secure = 1
func.private = 1
```
[^92]
**Annotation:** This excerpt demonstrates 'bytecode' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 6: Generators** *(pp.163–182)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^93]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Classes and Object-Oriented Programming** *(pp.183–228)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^94]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Modules and Packages** *(pp.229–256)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^95]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 6: Generators

*Source: Python Distilled, pages 163–182*

### Chapter Summary
Focuses on generators and iterators, covering yield statements, lazy evaluation, generator expressions, and the iteration protocol. Introduces coroutines and generator methods (send, throw, close). [^96]

### Concept-by-Concept Breakdown
#### **None** *(p.165)*

**Verbatim Educational Excerpt** *(Python Distilled, p.165, lines 5–12)*:
```
data = bytearray()
line = None
linecount = 0
while True:
part = yield line
linecount += part.count(b'\n')
data.extend(part)
if linecount > 0:
```
[^97]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.163)*

**Verbatim Educational Excerpt** *(Python Distilled, p.163, lines 31–38)*:
```
class Manager:
def __enter__(self):
return somevalue
def __exit__(self, ty, val, tb):
if ty:
# An exception occurred.
...
# Return True if handled, False otherwise
```
[^98]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.163)*

**Verbatim Educational Excerpt** *(Python Distilled, p.163, lines 33–40)*:
```
return somevalue
def __exit__(self, ty, val, tb):
if ty:
# An exception occurred.
...
# Return True if handled, False otherwise
With the @contextmanager generator, everything prior to the yield statement executes
when the manager enters (via the __enter__() method). Everything after the yield
```
[^99]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.176)*

**Verbatim Educational Excerpt** *(Python Distilled, p.176, lines 31–38)*:
```
class EvilAccount(Account):
def __init__(self, owner, balance, factor):
super().__init__(owner, balance)
self.factor = factor
def inquiry(self):
if random.randint(0,4) == 1:
return self.factor * super().inquiry()
else:
```
[^100]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.177)*

**Verbatim Educational Excerpt** *(Python Distilled, p.177, lines 33–40)*:
```
def __repr__(self):
return f'{type(self).__name__}({self.owner!r}, {self.balance!r})'
Now you’ll see more accurate output. Inheritance is not used with every class, but if it’s
an anticipated use case of the class you’re writing, you need to pay attention to details like
this. As a general rule, avoid the hardcoding of class names.
Inheritance establishes a relationship in the type system where any child class will
type-check as the parent class. For example:
>>> a = EvilAccount('Eva', 10)
```
[^101]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Repr__** *(p.177)*

**Verbatim Educational Excerpt** *(Python Distilled, p.177, lines 6–13)*:
```
child __init__() method.
Inheritance can break code in subtle ways. Consider the __repr__() method of the
Account class:
class Account:
def __init__(self, owner, balance):
self.owner = owner
self.balance = balance
def __repr__(self):
```
[^102]
**Annotation:** This excerpt demonstrates '__repr__' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Str__** *(p.175)*

**Verbatim Educational Excerpt** *(Python Distilled, p.175, lines 26–33)*:
```
is a class that is the root of all Python objects; it provides the default implementation of
some common methods such as __str__() and __repr__().
One use of inheritance is to extend an existing class with new methods. For example,
suppose you want to add a panic() method to Account that would withdraw all funds.
Here’s how:
class MyAcount(Account):
def panic(self):
self.withdraw(self.balance)
```
[^103]
**Annotation:** This excerpt demonstrates '__str__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.180)*

**Verbatim Educational Excerpt** *(Python Distilled, p.180, lines 26–33)*:
```
More broadly, making the internal list a hidden implementation detail is related to the
problem of data abstraction. Perhaps you later decide that you don’t even want to use
a list. The above design makes that easy to change. For example, if you change the
implementation to use linked tuples as follows, the users of Stack won’t even notice:
class Stack:
def __init__(self):
self._items = None
self._size = 0
```
[^104]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.169)*

**Verbatim Educational Excerpt** *(Python Distilled, p.169, lines 33–39)*:
```
The functions defined inside a class are known as methods. An instance method is a
function that operates on an instance of the class, which is passed as the first argument.
By convention, this argument is called self. In the preceding example, deposit(),
withdraw(), and inquiry() are examples of instance methods.
The __init__() and __repr__() methods of the class are examples of so-called special
or magic methods. These methods have special meaning to the interpreter runtime.
The __init__() method is used to initialize state when a new instance is created. The
```
[^105]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.165)*

**Verbatim Educational Excerpt** *(Python Distilled, p.165, lines 4–11)*:
```
def line_receiver():
data = bytearray()
line = None
linecount = 0
while True:
part = yield line
linecount += part.count(b'\n')
data.extend(part)
```
[^106]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.175)*

**Verbatim Educational Excerpt** *(Python Distilled, p.175, lines 2–9)*:
```
Chapter 7
Classes and Object-Oriented Programming
for account in port:
print(account)
# Access an individual account by index
port[1].inquiry()
# -> 50.0
The special methods that appear at the end, such as __len__(), __getitem__(), and
```
[^107]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 32 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.166)*

**Verbatim Educational Excerpt** *(Python Distilled, p.166, lines 13–20)*:
```
Generators and the Bridge to Awaiting
A classic use of generator functions is in libraries related to asynchronous I/O such as in
the standard asyncio module. However, since Python 3.5 much of this functionality has
been moved into a different language feature related to async functions and the await
statement (see the last part of Chapter 5).
The await statement involves interacting with a generator in disguise. Here is an
example that illustrates the underlying protocol used by await:
class Awaitable:
```
[^108]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Asyncio** *(p.166)*

**Verbatim Educational Excerpt** *(Python Distilled, p.166, lines 14–21)*:
```
A classic use of generator functions is in libraries related to asynchronous I/O such as in
the standard asyncio module. However, since Python 3.5 much of this functionality has
been moved into a different language feature related to async functions and the await
statement (see the last part of Chapter 5).
The await statement involves interacting with a generator in disguise. Here is an
example that illustrates the underlying protocol used by await:
class Awaitable:
def __await__(self):
```
[^109]
**Annotation:** This excerpt demonstrates 'asyncio' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.172)*

**Verbatim Educational Excerpt** *(Python Distilled, p.172, lines 1–8)*:
```
7.4 Attribute Access
157
'Guido'
>>> a.balance = 750.0
# set
>>> del a.balance
# delete
>>> a.balance
```
[^110]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Await** *(p.166)*

**Verbatim Educational Excerpt** *(Python Distilled, p.166, lines 1–8)*:
```
6.7 Generators and the Bridge to Awaiting
151
else:
return None
Although writing a class might be more familiar, the code is more complex and runs
slower. Tested on the author’s machine, feeding a large collection of chunks into a receiver
is about 40–50% faster with a generator than with this class code. Most of those savings are
due to the elimination of instance attribute lookup—local variables are faster.
```
[^111]
**Annotation:** This excerpt demonstrates 'await' as it appears in the primary text. The concept occurs 13 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 7: Classes and Object-Oriented Programming** *(pp.183–228)*

This later chapter builds upon the concepts introduced here, particularly: None, __enter__, __exit__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^112]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __enter__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Modules and Packages** *(pp.229–256)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __name__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^113]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Input/Output and Environment** *(pp.257–355)*

This later chapter builds upon the concepts introduced here, particularly: None, __enter__, __exit__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^114]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __enter__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 7: Classes and Object-Oriented Programming

*Source: Python Distilled, pages 183–228*

### Chapter Summary
In-depth exploration of object-oriented programming in Python, including class definition, inheritance, method resolution order, properties, metaclasses, and best practices for class design. [^115]

### Concept-by-Concept Breakdown
#### **Gil** *(p.208)*

**Verbatim Educational Excerpt** *(Python Distilled, p.208, lines 13–20)*:
```
raise RuntimeError('Unknown object')
Such a large if-elif-else block is inelegant and fragile. An often used solution is to
dispatch through a dictionary:
handlers = {
Duck: handle_duck,
Trombonist: handle_trombonist,
Cyclist: handle_cyclist
}
```
[^116]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Mro** *(p.205)*

**Verbatim Educational Excerpt** *(Python Distilled, p.205, lines 17–24)*:
```
First, whenever you use inheritance, Python builds a linear chain of classes known as
the Method Resolution Order, or MRO for short. This is available as the __mro__ attribute
on a class. Here are some examples for single inheritance:
class Base:
pass
class A(Base):
pass
class B(A):
```
[^117]
**Annotation:** This excerpt demonstrates 'MRO' as it appears in the primary text. The concept occurs 10 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.219)*

**Verbatim Educational Excerpt** *(Python Distilled, p.219, lines 32–39)*:
```
you need to call the weak reference as a function with no arguments. This will either
return the object being pointed at or None. For example:
acct = a_ref()
if acct is not None:
acct.withdraw(10)
# Alternative
if acct := a_ref():
acct.withdraw(10)
```
[^118]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.217)*

**Verbatim Educational Excerpt** *(Python Distilled, p.217, lines 38–42)*:
```
self.resource.close()
def __enter__(self):
return self
def __exit__(self, ty, val, tb):
self.close()
```
[^119]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.217)*

**Verbatim Educational Excerpt** *(Python Distilled, p.217, lines 40–42)*:
```
return self
def __exit__(self, ty, val, tb):
self.close()
```
[^120]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.215)*

**Verbatim Educational Excerpt** *(Python Distilled, p.215, lines 4–11)*:
```
The creation of an instance is carried out in two steps using the special method
__new__() that creates a new instance and __init__() that initializes it. For example, the
operation a = Account('Guido', 1000.0) performs these steps:
a = Account.__new__(Account, 'Guido', 1000.0)
if isinstance(a, Account):
Account.__init__('Guido', 1000.0)
Except for the first argument which is the class instead of an instance, __new__()
normally receives the same arguments as __init__(). However, the default
```
[^121]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.198)*

**Verbatim Educational Excerpt** *(Python Distilled, p.198, lines 22–29)*:
```
>>> s.yow
<bound method SomeClass.yow of <__main__.SomeClass object at 0x10e2572b0>>
>>>
How did this happen? It turns out that functions behave a lot like properties when
they’re placed in a class. Specifically, functions magically intercept attribute access and
create the bound method behind the scenes. When you define static and class methods
using @staticmethod and @classmethod, you are actually altering this process.
@staticmethod returns the method function back “as is” without any special wrapping or
```
[^122]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.211)*

**Verbatim Educational Excerpt** *(Python Distilled, p.211, lines 15–22)*:
```
def __repr__(self):
return f'{type(self).__name__}({self.x!r}, {self.y!r})'
Writing such methods is often annoying. Perhaps a class decorator could create the
method for you?
import inspect
def with_repr(cls):
args = list(inspect.signature(cls).parameters)
argvals = ', '.join('{self.%s!r}' % arg for arg in args)
```
[^123]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Repr__** *(p.211)*

**Verbatim Educational Excerpt** *(Python Distilled, p.211, lines 9–16)*:
```
Class decorators can also be used to create entirely new code. For example, a common
task when writing a class is to write a useful __repr__() method for improved debugging:
class Point:
def __init__(self, x, y):
self.x = x
self.y = y
def __repr__(self):
return f'{type(self).__name__}({self.x!r}, {self.y!r})'
```
[^124]
**Annotation:** This excerpt demonstrates '__repr__' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Str__** *(p.186)*

**Verbatim Educational Excerpt** *(Python Distilled, p.186, lines 25–32)*:
```
self.day = day
def __str__(self):
return self.datefmt.format(year=self.year,
month=self.month,
day=self.day)
@classmethod
def from_timestamp(cls, ts):
tm = time.localtime(ts)
```
[^125]
**Annotation:** This excerpt demonstrates '__str__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.211)*

**Verbatim Educational Excerpt** *(Python Distilled, p.211, lines 20–27)*:
```
def with_repr(cls):
args = list(inspect.signature(cls).parameters)
argvals = ', '.join('{self.%s!r}' % arg for arg in args)
code = 'def __repr__(self):\n'
code += f'
return f"{cls.__name__}({argvals})"\n'
locs = { }
exec(code, locs)
```
[^126]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.186)*

**Verbatim Educational Excerpt** *(Python Distilled, p.186, lines 2–9)*:
```
171
The first argument of a class method is always the class itself. By convention, this
argument is often named cls. In this example, cls is set to Account. If the purpose of a
class method is to create a new instance, explicit steps must be taken to do so. In the final
line of the example, the call cls(..., ...) is the same as calling Account(..., ...) on
the two arguments.
The fact that the class is passed as argument solves an important problem related to
inheritance. Suppose you define a subclass of Account and now want to create an instance
```
[^127]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.225)*

**Verbatim Educational Excerpt** *(Python Distilled, p.225, lines 35–41)*:
```
a dictionary for storing instance data. Instead, a much more compact data structure based
on an array is used. In programs that create a large number of objects, using __slots__
can result in a substantial reduction in memory use and a modest improvement in
execution time.
The only entries in __slots__ are instance attributes. You do not list methods,
properties, class variables, or any other class-level attributes. Basically, it’s the same names
that would ordinarily appear as dictionary keys in the instance’s __dict__.
```
[^128]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.205)*

**Verbatim Educational Excerpt** *(Python Distilled, p.205, lines 2–9)*:
```
Chapter 7
Classes and Object-Oriented Programming
class AnnoyingLoudCyclist(AnnoyingMixin, LoudMixin, Cyclist):
pass
d = LoudDuck()
d.noise() # -> 'QUACK'
t = AnnoyingTrombonist()
t.noise() # -> 'Blat!Blat!Blat!'
```
[^129]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 47 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.216)*

**Verbatim Educational Excerpt** *(Python Distilled, p.216, lines 19–26)*:
```
e = Date(2012, 12, 21)
assert d is e
# Same object
In this example, the class keeps an internal dictionary of previously created Date
instances. When creating a new Date, the cache is consulted first. If a match is found, that
instance is returned. Otherwise, a new instance is created and initialized.
A subtle detail of this solution is the empty __init__() method. Even though instances
are cached, every call to Date() still invokes __init__(). To avoid duplicated effort, the
```
[^130]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 8: Modules and Packages** *(pp.229–256)*

This later chapter builds upon the concepts introduced here, particularly: GIL, MRO, None.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^131]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, MRO appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Input/Output and Environment** *(pp.257–355)*

This later chapter builds upon the concepts introduced here, particularly: MRO, None, __enter__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^132]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts MRO, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 8: Modules and Packages

*Source: Python Distilled, pages 229–256*

### Chapter Summary
Covers Python's module and package system including import mechanisms, namespace management, package structure, module search path, and package initialization with __init__.py files. [^133]

### Concept-by-Concept Breakdown
#### **Gil** *(p.252)*

**Verbatim Educational Excerpt** *(Python Distilled, p.252, lines 15–22)*:
```
from graphics.primitives import lines
Sadly, writing out a full package name like that is both annoying and fragile. For
example, sometimes it makes sense to rename a package—maybe you want to rename it so
that you can use different versions. If the package name is hardwired into the code, you
can’t do that. A better choice is to use a package-relative import like this:
# graphics/primitives/fill.py
# Package-relative import
from . import lines
```
[^134]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Mro** *(p.237)*

**Verbatim Educational Excerpt** *(Python Distilled, p.237, lines 35–42)*:
```
Tuple of base classes
cls.__mro__
Method Resolution Order tuple
cls.__dict__
Dictionary holding class methods and variables
cls.__doc__
Documentation string
cls.__annotations__
```
[^135]
**Annotation:** This excerpt demonstrates 'MRO' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.248)*

**Verbatim Educational Excerpt** *(Python Distilled, p.248, lines 36–40)*:
```
Dataclasses work by generating method functions as text fragments and executing
them using exec(). None of this generated code is cached by the import system. For a
single class definition, you won’t notice. However, if you have a module consisting of
100 dataclasses, you might find that it imports nearly 20 times slower than a comparable
module where you just wrote out the classes in the normal, if less compact, way.
```
[^136]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Pythonpath** *(p.249)*

**Verbatim Educational Excerpt** *(Python Distilled, p.249, lines 11–18)*:
```
determines the search order used when importing modules. To add new entries to the
search path, add them to this list. This can be done directly or by setting the PYTHONPATH
environment variable. For example, on UNIX:
bash $ env PYTHONPATH=/some/path python3 script.py
ZIP archive files are a convenient way to bundle a collection of modules into a single
file. For example, suppose you created two modules, foo.py and bar.py, and placed them
in a file mymodules.zip. The file could be added to the Python search path as follows:
import sys
```
[^137]
**Annotation:** This excerpt demonstrates 'PYTHONPATH' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.256)*

**Verbatim Educational Excerpt** *(Python Distilled, p.256, lines 37–40)*:
```
'resources/data.json')
textdata = rawdata.decode('utf-8')
data = json.loads(textdata)
print(data)
```
[^138]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.251)*

**Verbatim Educational Excerpt** *(Python Distilled, p.251, lines 5–12)*:
```
graph2d/
__init__.py
plot2d.py
...
graph3d/
__init__.py
plot3d.py
...
```
[^139]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 10 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.250)*

**Verbatim Educational Excerpt** *(Python Distilled, p.250, lines 5–12)*:
```
# Check if running as a program
if __name__ == '__main__':
# Yes. Running as the main script
statements
else:
# No, I must have been imported as a module
statements
Source files intended for use as libraries can use this technique to include optional
```
[^140]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.237)*

**Verbatim Educational Excerpt** *(Python Distilled, p.237, lines 27–34)*:
```
Description
cls.__name__
Class name
cls.__module__
Module name in which the class is defined
cls.__qualname__
Fully qualified class name
cls.__bases__
```
[^141]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.238)*

**Verbatim Educational Excerpt** *(Python Distilled, p.238, lines 24–28)*:
```
qualities. First and foremost, readability counts for a lot—and it often suffers if you pile on
too many layers of abstraction. Second, you should try to make code that is easy to observe
and debug, and don’t forget about using the REPL. Finally, making code testable is often a
good driver for good design. If your code can’t be tested or testing is too awkward, there
may be a better way to organize your solution.
```
[^142]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Annotation** *(p.237)*

**Verbatim Educational Excerpt** *(Python Distilled, p.237, lines 41–48)*:
```
Documentation string
cls.__annotations__
Dictionary of class type hints
cls.__abstractmethods__
Set of abstract method names (may be undefined if there
aren’t any).
The cls.__name__ attribute contains a short class name. The cls.__qualname__
attribute contains a fully qualified name with additional information about the
```
[^143]
**Annotation:** This excerpt demonstrates 'annotation' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.234)*

**Verbatim Educational Excerpt** *(Python Distilled, p.234, lines 32–39)*:
```
# Creates new instances of the class
def __call__(cls, *args, **kwargs):
print("Creating instance:", args, kwargs)
return super().__call__(*args, **kwargs)
# Example
class Base(metaclass=mytype):
pass
# Definition of the Base produces the following output
```
[^144]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.231)*

**Verbatim Educational Excerpt** *(Python Distilled, p.231, lines 32–38)*:
```
function responsible for populating the class namespace. This callback receives the class
namespace dictionary as an argument. It should update this dictionary in place. The return
value of the callback is ignored.
Dynamic class creation may be useful if you want to create classes from data structures.
For example, in the section on descriptors, the following classes were defined:
class Integer(Typed):
expected_type = int
```
[^145]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.234)*

**Verbatim Educational Excerpt** *(Python Distilled, p.234, lines 1–8)*:
```
7.31 Metaclasses
219
class Account(metaclass=type):
...
If no metaclass is given, the class statement examines the type of the first entry in the
tuple of base classes (if any) and uses that as the metaclass. Therefore, if you write class
Account(object), the resulting Account class will have the same type as object (which is
type). Note that classes that don’t specify any parent at all always inherit from object, so
```
[^146]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 43 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.237)*

**Verbatim Educational Excerpt** *(Python Distilled, p.237, lines 22–29)*:
```
needs to directly manipulate types.
Table 7.1 shows commonly used attributes of a type object cls.
Table 7.1
Attributes of Types
Attribute
Description
cls.__name__
Class name
```
[^147]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Bytecode** *(p.248)*

**Verbatim Educational Excerpt** *(Python Distilled, p.248, lines 12–19)*:
```
Module Compilation
When modules are first imported, they are compiled into an interpreter bytecode. This
code is written to a .pyc file within a special __pycache__ directory. This directory is
usually found in the same directory as the original .py file. When the same import occurs
again on a different run of the program, the compiled bytecode is loaded instead. This
significantly speeds up the import process.
The caching of bytecode is an automatic process that you almost never need to worry
about. Files are automatically regenerated if the original source code changes. It just works.
```
[^148]
**Annotation:** This excerpt demonstrates 'bytecode' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 9: Input/Output and Environment** *(pp.257–355)*

This later chapter builds upon the concepts introduced here, particularly: MRO, None, PYTHONPATH.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^149]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts MRO, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 9: Input/Output and Environment

*Source: Python Distilled, pages 257–355*

### Chapter Summary
Examines input/output operations including file handling, path manipulation, directory operations, environment variables, and standard streams (stdin, stdout, stderr). Covers both text and binary I/O with proper encoding handling. [^150]

### Concept-by-Concept Breakdown
#### **Mro** *(p.345)*

**Verbatim Educational Excerpt** *(Python Distilled, p.345, lines 22–29)*:
```
metaclasses, 217–222
Method Resolution Order (MRO, 190–192, 222 
methods, 79, 154
abstract, 185, 222
available on an object, 26
bound, 158, 183
decorating automatically, 222
defining, 215
```
[^151]
**Annotation:** This excerpt demonstrates 'MRO' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.282)*

**Verbatim Educational Excerpt** *(Python Distilled, p.282, lines 3–10)*:
```
>>> r = line_receiver()
>>> r.send(None)
# Necessary first step
>>> r.send(b'hello')
>>> r.send(b'world\nit ')
b'hello world\n'
>>> r.send(b'works!')
>>> r.send(b'\n')
```
[^152]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Pythonpath** *(p.347)*

**Verbatim Educational Excerpt** *(Python Distilled, p.347, lines 71–78)*:
```
python shell, 1
PYTHONPATH environment variable, 234
__qualname__ attribute, 129, 222
__qualname__ variable, 215
Queue class, 292
quit(), in REPL, 2
__radd__() method, 90–91
raise statement, 25, 64, 69
```
[^153]
**Annotation:** This excerpt demonstrates 'PYTHONPATH' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.265)*

**Verbatim Educational Excerpt** *(Python Distilled, p.265, lines 4–11)*:
```
>>> a = b'Spicy Jalape\xf1o'
# Invalid UTF-8
>>> a.decode('utf-8')
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf1
in position 12: invalid continuation byte
>>> a.decode('utf-8', 'surrogateescape')
```
[^154]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.340)*

**Verbatim Educational Excerpt** *(Python Distilled, p.340, lines 43–50)*:
```
endswith() method, 10, 298, 311
__enter__() method, 75, 99, 148
enumerate() function, 61, 303
env command, 256
environment variables, 256
EnvironmentError exception, 314–316
EOF (end of file) character, 2, 68, 315
EOFError exception, 68, 315
```
[^155]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Eq__** *(p.340)*

**Verbatim Educational Excerpt** *(Python Distilled, p.340, lines 51–58)*:
```
epoll() function, 285
__eq__() method, 93–94
errno attribute, 316
errno module, 277–278
errors
handling, 110–111
logging, 66
errors attribute, 259–260, 263
```
[^156]
**Annotation:** This excerpt demonstrates '__eq__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.340)*

**Verbatim Educational Excerpt** *(Python Distilled, p.340, lines 84–91)*:
```
exec() function, 133–134, 233, 301, 303
__exit__() method, 75, 99, 148
expandtabs() method, 298, 311
expressions, 3, 38–39
evaluating, 43, 303
extend() method, 300, 307
Extensible Markup Language (XML), 295
f-strings, 4, 9, 11, 251–252
```
[^157]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.343)*

**Verbatim Educational Excerpt** *(Python Distilled, p.343, lines 14–21)*:
```
INI files, 276
__init__() method, 27, 70, 89, 134, 154–155,
161, 181–201, 219–220
__init__.py file, 34–35, 235–237, 239–241
__init_subclass__() method, 197–199, 220–222
input() function, 13, 33, 304, 315
input/output (I/O), 247–296
buffering, 258–260
```
[^158]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.260)*

**Verbatim Educational Excerpt** *(Python Distilled, p.260, lines 9–16)*:
```
__init__.py
__main__.py
Put your starting code in __main__.py and run your program using a command such
as python -m program. As you need more code, add new files to your package and use
package-relative imports. An advantage of using a package is that all of your code remains
isolated. You can name the files whatever you want and not worry about collisions with
other packages, standard library modules, or code written by your coworkers. Although
setting up a package requires a bit more work at the start, it will likely save you a lot of
```
[^159]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.257)*

**Verbatim Educational Excerpt** *(Python Distilled, p.257, lines 17–24)*:
```
Description
__name__
Full module name
__doc__
Documentation string
__dict__
Module dictionary
__file__
```
[^160]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Repr__** *(p.339)*

**Verbatim Educational Excerpt** *(Python Distilled, p.339, lines 48–55)*:
```
with repr(), 11
with __repr__(), 28, 196
decode() method, 248, 259, 298, 310
decorators, 104, 124–127, 194–197, 220
deep copies, 83
deepcopy() function, 84
def statement, 22, 27, 101
DEFAULT_BUFFER_SIZE value, 259
```
[^161]
**Annotation:** This excerpt demonstrates '__repr__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Str__** *(p.325)*

**Verbatim Educational Excerpt** *(Python Distilled, p.325, lines 19–26)*:
```
Type representing a string. If object is supplied, a string representation of its value is
created by calling its __str__() method. This is the same string that you see when
you print the object. If no argument is given, an empty string is created.
Table 10.9 shows methods defined on strings.
Table 10.9
String Operators and Methods
Operation
Description
```
[^162]
**Annotation:** This excerpt demonstrates '__str__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.262)*

**Verbatim Educational Excerpt** *(Python Distilled, p.262, lines 5–12)*:
```
I/O, and data serialization. Particular attention is given to programming techniques and
abstractions that encourage proper I/O handling. The end of this chapter gives an
overview of common standard library modules related to I/O.
9.1
Data Representation
The main problem of I/O is the outside world. To communicate with it, data must be
properly represented, so that it can be manipulated. At the lowest level, Python works with
two fundamental datatypes: bytes that represent raw uninterpreted data of any kind and text
```
[^163]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Annotation** *(p.257)*

**Verbatim Educational Excerpt** *(Python Distilled, p.257, lines 29–36)*:
```
List of subdirectories to search for submodules of a package.
__annotations__
Module-level type hints
The __dict__ attribute is a dictionary that represents the module namespace.
Everything that’s defined in the module is placed here.
The __name__ attribute is often used in scripts. A check such as if __name__ ==
'__main__' is often done to see if a file is running as a standalone program.
The __package__ attribute contains the name of the enclosing package if any. If set,
```
[^164]
**Annotation:** This excerpt demonstrates 'annotation' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argparse** *(p.270)*

**Verbatim Educational Excerpt** *(Python Distilled, p.270, lines 6–13)*:
```
Although in simple scripts, you can manually process command options, consider using
the argparse module for more complicated command-line handling. Here is an example:
import argparse
def main(argv):
p = argparse.ArgumentParser(description="This is some program")
# A positional argument
p.add_argument("infile")
# An option taking an argument
```
[^165]
**Annotation:** This excerpt demonstrates 'argparse' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---


---

### **Footnotes**

[^1]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 1, lines 1–25).
[^2]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 8, lines 25–32).
[^3]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 17, lines 33–38).
[^4]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 8, lines 30–37).
[^5]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 38, lines 16–23).
[^6]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 8, lines 67–74).
[^7]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 31, lines 32–39).
[^8]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 40, lines 3–10).
[^9]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 7, lines 90–95).
[^10]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 7, lines 90–95).
[^11]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 12, lines 25–32).
[^12]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 12, lines 25–32).
[^13]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 9, lines 17–24).
[^14]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 9, lines 26–33).
[^15]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 21, lines 50–56).
[^16]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 27, lines 31–38).
[^17]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 41, lines 1–1).
[^18]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 63, lines 1–1).
[^19]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 89, lines 1–1).
[^20]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 41, lines 1–25).
[^21]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 59, lines 5–12).
[^22]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 42, lines 12–19).
[^23]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 48, lines 2–9).
[^24]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 48, lines 2–9).
[^25]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 43, lines 7–14).
[^26]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 48, lines 35–41).
[^27]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 59, lines 10–17).
[^28]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 51, lines 34–40).
[^29]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 53, lines 3–10).
[^30]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 42, lines 25–32).
[^31]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 58, lines 1–8).
[^32]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 51, lines 18–25).
[^33]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 42, lines 1–8).
[^34]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 41, lines 13–20).
[^35]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 50, lines 2–9).
[^36]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 63, lines 1–1).
[^37]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 89, lines 1–1).
[^38]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 125, lines 1–1).
[^39]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 63, lines 1–25).
[^40]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 69, lines 12–19).
[^41]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 85, lines 3–10).
[^42]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 86, lines 18–25).
[^43]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 71, lines 22–29).
[^44]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 71, lines 3–10).
[^45]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 73, lines 16–23).
[^46]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 83, lines 5–12).
[^47]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 83, lines 30–37).
[^48]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 83, lines 30–37).
[^49]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 84, lines 12–19).
[^50]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 88, lines 6–13).
[^51]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 73, lines 6–13).
[^52]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 78, lines 10–17).
[^53]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 83, lines 5–12).
[^54]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 81, lines 26–33).
[^55]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 89, lines 1–1).
[^56]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 125, lines 1–1).
[^57]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 163, lines 1–1).
[^58]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 89, lines 1–25).
[^59]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 102, lines 14–21).
[^60]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 105, lines 13–20).
[^61]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 90, lines 30–37).
[^62]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 108, lines 8–15).
[^63]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 114, lines 17–24).
[^64]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 104, lines 16–23).
[^65]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 121, lines 18–25).
[^66]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 104, lines 21–28).
[^67]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 109, lines 27–34).
[^68]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 102, lines 1–8).
[^69]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 122, lines 12–19).
[^70]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 119, lines 34–41).
[^71]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 118, lines 1–8).
[^72]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 103, lines 15–22).
[^73]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 90, lines 2–9).
[^74]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 125, lines 1–1).
[^75]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 163, lines 1–1).
[^76]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 183, lines 1–1).
[^77]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 125, lines 1–25).
[^78]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 125, lines 14–21).
[^79]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 149, lines 26–33).
[^80]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 141, lines 7–14).
[^81]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 160, lines 21–28).
[^82]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 144, lines 22–29).
[^83]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 136, lines 7–14).
[^84]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 135, lines 7–14).
[^85]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 151, lines 3–10).
[^86]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 146, lines 13–20).
[^87]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 150, lines 1–8).
[^88]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 150, lines 6–13).
[^89]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 144, lines 1–8).
[^90]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 151, lines 7–14).
[^91]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 156, lines 16–23).
[^92]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 145, lines 5–12).
[^93]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 163, lines 1–1).
[^94]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 183, lines 1–1).
[^95]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 229, lines 1–1).
[^96]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 163, lines 1–25).
[^97]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 165, lines 5–12).
[^98]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 163, lines 31–38).
[^99]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 163, lines 33–40).
[^100]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 176, lines 31–38).
[^101]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 177, lines 33–40).
[^102]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 177, lines 6–13).
[^103]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 175, lines 26–33).
[^104]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 180, lines 26–33).
[^105]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 169, lines 33–39).
[^106]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 165, lines 4–11).
[^107]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 175, lines 2–9).
[^108]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 166, lines 13–20).
[^109]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 166, lines 14–21).
[^110]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 172, lines 1–8).
[^111]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 166, lines 1–8).
[^112]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 183, lines 1–1).
[^113]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 229, lines 1–1).
[^114]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 257, lines 1–1).
[^115]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 183, lines 1–25).
[^116]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 208, lines 13–20).
[^117]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 205, lines 17–24).
[^118]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 219, lines 32–39).
[^119]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 217, lines 38–42).
[^120]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 217, lines 40–42).
[^121]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 215, lines 4–11).
[^122]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 198, lines 22–29).
[^123]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 211, lines 15–22).
[^124]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 211, lines 9–16).
[^125]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 186, lines 25–32).
[^126]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 211, lines 20–27).
[^127]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 186, lines 2–9).
[^128]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 225, lines 35–41).
[^129]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 205, lines 2–9).
[^130]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 216, lines 19–26).
[^131]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 229, lines 1–1).
[^132]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 257, lines 1–1).
[^133]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 229, lines 1–25).
[^134]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 252, lines 15–22).
[^135]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 237, lines 35–42).
[^136]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 248, lines 36–40).
[^137]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 249, lines 11–18).
[^138]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 256, lines 37–40).
[^139]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 251, lines 5–12).
[^140]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 250, lines 5–12).
[^141]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 237, lines 27–34).
[^142]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 238, lines 24–28).
[^143]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 237, lines 41–48).
[^144]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 234, lines 32–39).
[^145]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 231, lines 32–38).
[^146]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 234, lines 1–8).
[^147]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 237, lines 22–29).
[^148]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 248, lines 12–19).
[^149]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 257, lines 1–1).
[^150]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 257, lines 1–25).
[^151]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 345, lines 22–29).
[^152]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 282, lines 3–10).
[^153]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 347, lines 71–78).
[^154]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 265, lines 4–11).
[^155]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 340, lines 43–50).
[^156]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 340, lines 51–58).
[^157]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 340, lines 84–91).
[^158]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 343, lines 14–21).
[^159]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 260, lines 9–16).
[^160]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 257, lines 17–24).
[^161]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 339, lines 48–55).
[^162]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 325, lines 19–26).
[^163]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 262, lines 5–12).
[^164]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 257, lines 29–36).
[^165]: Beazley, David. *Python Distilled*. (JSON `Python Distilled.json`, p. 270, lines 6–13).
