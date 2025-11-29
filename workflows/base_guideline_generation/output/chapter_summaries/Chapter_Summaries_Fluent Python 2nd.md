# Comprehensive Python Guidelines — Python Cookbook, 3rd Edition (Chapters 1-15)

*Source: Python Cookbook, 3rd Edition, Chapters 1-15*

---

## Chapter 1: Data Structures and Algorithms

*Source: Python Cookbook, 3rd Edition, pages 1–36*

### Chapter Summary
Recipes for Mastering Python 3

O’REILLY° David Beazley & Brian K Key topics include functions, strings, and modules. Covers dict, file, function. [^1]

### Concept-by-Concept Breakdown
#### **Gil** *(p.10)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.10, lines 32–39)*:
```
12.8. Performing Simple Parallel Programming                                                       509
12.9. Dealing with the GIL (and How to Stop Worrying About It)                        513
12.10. Defining an Actor Task                                                                                      516
12.11. Implementing Publish/Subscribe Messaging                                                 520
12.12. Using Generators As an Alternative to Threads                                            524
12.13. Polling Multiple Thread Queues                                                                      531
12.14. Launching a Daemon Process on Unix                                                           534
13. Utility Scripting and System Administration. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  539
```
[^2]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.35)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.35, lines 22–29)*:
```
change to this recipe, as follows:
def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)
```
[^3]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.27)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.27, lines 4–11)*:
```
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0
    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1
    def pop(self):
```
[^4]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.24)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.24, lines 8–15)*:
```
# Example use on a file
if __name__ == '__main__':
    with open('somefile.txt') as f:
        for line, prevlines in search(f, 'python', 5):
            for pline in prevlines:
                print(pline, end='')
            print(line, end='')
            print('-'*20)
```
[^5]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.24)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.24, lines 8–15)*:
```
# Example use on a file
if __name__ == '__main__':
    with open('somefile.txt') as f:
        for line, prevlines in search(f, 'python', 5):
            for pline in prevlines:
                print(pline, end='')
            print(line, end='')
            print('-'*20)
```
[^6]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Repr__** *(p.27)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.27, lines 16–23)*:
```
...         self.name = name
...     def __repr__(self):
...         return 'Item({!r})'.format(self.name)
...
>>> q = PriorityQueue()
>>> q.push(Item('foo'), 1)
>>> q.push(Item('bar'), 5)
>>> q.push(Item('spam'), 4)
```
[^7]
**Annotation:** This excerpt demonstrates '__repr__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Annotation** *(p.9)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.9, lines 26–33)*:
```
9.19. Initializing Class Members at Definition Time                                                374
9.20. Implementing Multiple Dispatch with Function Annotations                      376
9.21. Avoiding Repetitive Property Methods                                                             382
9.22. Defining Context Managers the Easy Way                                                       384
9.23. Executing Code with Local Side Effects                                                            386
9.24. Parsing and Analyzing Python Source                                                              388
9.25. Disassembling Python Byte Code                                                                      392
10. Modules and Packages. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  397
```
[^8]
**Annotation:** This excerpt demonstrates 'annotation' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.22)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.22, lines 22–29)*:
```
    print('bar', s)
for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)
Star unpacking can also be useful when combined with certain kinds of string processing
operations, such as splitting. For example:
```
[^9]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.8)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.8, lines 7–14)*:
```
7. Functions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  217
7.1. Writing Functions That Accept Any Number of Arguments                           217
7.2. Writing Functions That Only Accept Keyword Arguments                            219
7.3. Attaching Informational Metadata to Function Arguments                            220
7.4. Returning Multiple Values from a Function                                                       221
7.5. Defining Functions with Default Arguments                                                     222
7.6. Defining Anonymous or Inline Functions                                                         224
7.7. Capturing Variables in Anonymous Functions                                                  225
```
[^10]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.6)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.6, lines 25–32)*:
```
3.8. Calculating with Fractions                                                                                      96
3.9. Calculating with Large Numerical Arrays                                                             97
3.10. Performing Matrix and Linear Algebra Calculations                                      100
3.11. Picking Things at Random                                                                                  102
3.12. Converting Days to Seconds, and Other Basic Time Conversions               104
3.13. Determining Last Friday’s Date                                                                          106
3.14. Finding the Date Range for the Current Month                                              107
3.15. Converting Strings into Datetimes                                                                    109
```
[^11]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.9)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.9, lines 1–8)*:
```
8.20. Calling a Method on an Object Given the Name As a String                        305
8.21. Implementing the Visitor Pattern                                                                      306
8.22. Implementing the Visitor Pattern Without Recursion                                   311
8.23. Managing Memory in Cyclic Data Structures                                                  317
8.24. Making Classes Support Comparison Operations                                          321
8.25. Creating Cached Instances                                                                                  323
9. Metaprogramming. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  329
9.1. Putting a Wrapper Around a Function                                                               329
```
[^12]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 16 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.8)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.8, lines 26–33)*:
```
8.5. Encapsulating Names in a Class                                                                           250
8.6. Creating Managed Attributes                                                                               251
8.7. Calling a Method on a Parent Class                                                                     256
8.8. Extending a Property in a Subclass                                                                      260
8.9. Creating a New Kind of Class or Instance Attribute                                         264
8.10. Using Lazily Computed Properties                                                                    267
8.11. Simplifying the Initialization of Data Structures                                             270
8.12. Defining an Interface or Abstract Base Class                                                   274
```
[^13]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.9)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.9, lines 4–11)*:
```
8.23. Managing Memory in Cyclic Data Structures                                                  317
8.24. Making Classes Support Comparison Operations                                          321
8.25. Creating Cached Instances                                                                                  323
9. Metaprogramming. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  329
9.1. Putting a Wrapper Around a Function                                                               329
9.2. Preserving Function Metadata When Writing Decorators                              331
9.3. Unwrapping a Decorator                                                                                       333
9.4. Defining a Decorator That Takes Arguments                                                    334
```
[^14]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 11 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.26)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.26, lines 26–33)*:
```
implementation of nlargest() and nsmallest() is adaptive in how it operates and will
carry out some of these optimizations on your behalf (e.g., using sorting if N is close to
the same size as the input).
Although it’s not necessary to use this recipe, the implementation of a heap is an inter‐
esting and worthwhile subject of study. This can usually be found in any decent book
on algorithms and data structures. The documentation for the heapq module also dis‐
cusses the underlying implementation details.
1.5. Implementing a Priority Queue
```
[^15]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Closure** *(p.8)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.8, lines 19–26)*:
```
7.11. Inlining Callback Functions                                                                                235
7.12. Accessing Variables Defined Inside a Closure                                                 238
8. Classes and Objects. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  243
8.1. Changing the String Representation of Instances                                              243
8.2. Customizing String Formatting                                                                            245
8.3. Making Objects Support the Context-Management Protocol                         246
8.4. Saving Memory When Creating a Large Number of Instances                       248
8.5. Encapsulating Names in a Class                                                                           250
```
[^16]
**Annotation:** This excerpt demonstrates 'closure' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 2: Strings and Text** *(pp.37–82)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __repr__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^17]

**Annotation:** Forward reference: Chapter 2 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 3: Numbers, Dates, and Times** *(pp.83–112)*

This later chapter builds upon the concepts introduced here, particularly: None, argument, array.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^18]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, argument appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Iterators and Generators** *(pp.113–140)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^19]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 2: Strings and Text

*Source: Python Cookbook, 3rd Edition, pages 37–82*

### Chapter Summary
Under the
covers, a Counter is a dictionary that maps the items to the number of occurrences Key topics include strings, function, and object. Covers string, dict, method. [^20]

### Concept-by-Concept Breakdown
#### **None** *(p.50)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.50, lines 3–10)*:
```
>>> dict_to_stock(a)
Stock(name='ACME', shares=100, price=123.45, date=None, time=None)
>>> b = {'name': 'ACME', 'shares': 100, 'price': 123.45, 'date': '12/17/2012'}
>>> dict_to_stock(b)
Stock(name='ACME', shares=100, price=123.45, date='12/17/2012', time=None)
>>>
Last, but not least, it should be noted that if your goal is to define an efficient data
structure where you will be changing various instance attributes, using namedtuple is
```
[^21]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.41)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.41, lines 33–38)*:
```
>>> class User:
...     def __init__(self, user_id):
...         self.user_id = user_id
1.14. Sorting Objects Without Native Comparison Support 
| 
23
```
[^22]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Repr__** *(p.42)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.42, lines 1–8)*:
```
...     def __repr__(self):
...         return 'User({})'.format(self.user_id)
...
>>> users = [User(23), User(3), User(99)]
>>> users
[User(23), User(3), User(99)]
>>> sorted(users, key=lambda u: u.user_id)
[User(3), User(23), User(99)]
```
[^23]
**Annotation:** This excerpt demonstrates '__repr__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.51)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.51, lines 5–12)*:
```
The solution shows a subtle syntactic aspect of generator expressions when supplied as
the single argument to a function (i.e., you don’t need repeated parentheses). For ex‐
ample, these statements are the same:
s = sum((x * x for x in nums))    # Pass generator-expr as argument
s = sum(x * x for x in nums)      # More elegant syntax
Using a generator argument is often a more efficient and elegant approach than first
creating a temporary list. For example, if you didn’t use a generator expression, you
might consider this alternative implementation:
```
[^24]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.41)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.41, lines 1–8)*:
```
from rows as input and returns a value that will be used as the basis for sorting. The
itemgetter() function creates just such a callable.
The operator.itemgetter() function takes as arguments the lookup indices used to
extract the desired values from the records in rows. It can be a dictionary key name, a
numeric list element, or any value that can be fed to an object’s __getitem__() method.
If you give multiple indices to itemgetter(), the callable it produces will return a tuple
with all of the elements in it, and sorted() will order the output according to the sorted
order of the tuples. This can be useful if you want to simultaneously sort on multiple
```
[^25]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 15 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.49)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.49, lines 19–26)*:
```
  File "<stdin>", line 1, in <module>
AttributeError: can't set attribute
>>>
If you need to change any of the attributes, it can be done using the _replace() method
of a namedtuple instance, which makes an entirely new namedtuple with specified val‐
ues replaced. For example:
>>> s = s._replace(shares=75)
>>> s
```
[^26]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.46)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.46, lines 3–10)*:
```
Another notable filtering tool is itertools.compress(), which takes an iterable and
an accompanying Boolean selector sequence as input. As output, it gives you all of the
items in the iterable where the corresponding element in the selector is True. This can
be useful if you’re trying to apply the results of filtering one sequence to another related
sequence. For example, suppose you have the following two columns of data:
addresses = [
    '5412 N CLARK',
    '5148 N CLARK',
```
[^27]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.48)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.48, lines 29–36)*:
```
elements it manipulates. So, if you get back a large list of tuples from a database call,
then manipulate them by accessing the positional elements, your code could break if,
say, you added a new column to your table. Not so if you first cast the returned tuples
to namedtuples.
To illustrate, here is some code using ordinary tuples:
def compute_cost(records):
    total = 0.0
    for rec in records:
```
[^28]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.80)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.80, lines 8–15)*:
```
One subtle feature of vars() is that it also works with instances. For example:
>>> class Info:
...     def __init__(self, name, n):
...         self.name = name
...         self.n = n
...
>>> a = Info('Guido',37)
>>> s.format_map(vars(a))
```
[^29]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.66)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.66, lines 1–8)*:
```
Solution
This problem often arises in patterns that try to match text enclosed inside a pair of
starting and ending delimiters (e.g., a quoted string). To illustrate, consider this example:
>>> str_pat = re.compile(r'\"(.*)\"')
>>> text1 = 'Computer says "no."'
>>> str_pat.findall(text1)
['no.']
>>> text2 = 'Computer says "no." Phone says "yes."'
```
[^30]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.48)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.48, lines 1–8)*:
```
Solution
collections.namedtuple() provides these benefits, while adding minimal overhead
over using a normal tuple object. collections.namedtuple() is actually a factory
method that returns a subclass of the standard Python tuple type. You feed it a type
name, and the fields it should have, and it returns a class that you can instantiate, passing
in values for the fields you’ve defined, and so on. For example:
>>> from collections import namedtuple
>>> Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
```
[^31]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Compiled** *(p.63)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.63, lines 13–20)*:
```
pays to compile the pattern first and use it over and over again. The module-level func‐
tions keep a cache of recently compiled patterns, so there isn’t a huge performance hit,
but you’ll save a few lookups and extra processing by using your own compiled pattern.
2.5. Searching and Replacing Text
Problem
You want to search for and replace a text pattern in a string.
Solution
For simple literal patterns, use the str.replace() method. For example:
```
[^32]
**Annotation:** This excerpt demonstrates 'compiled' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Comprehension** *(p.47)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.47, lines 1–8)*:
```
Solution
This is easily accomplished using a dictionary comprehension. For example:
prices = {
   'ACME': 45.23,
   'AAPL': 612.78,
   'IBM': 205.55,
   'HPQ': 37.20,
   'FB': 10.75
```
[^33]
**Annotation:** This excerpt demonstrates 'comprehension' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.59)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.59, lines 1–8)*:
```
True
>>> names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'foo.py']
>>> [name for name in names if fnmatch(name, 'Dat*.csv')]
['Dat1.csv', 'Dat2.csv']
>>>
Normally, fnmatch() matches patterns using the same case-sensitivity rules as the sys‐
tem’s underlying filesystem (which varies based on operating system). For example:
>>> # On OS X (Mac)
```
[^34]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Debugging** *(p.81)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.81, lines 34–41)*:
```
would see the missing values appearing in the resulting string (potentially useful for
debugging).
The sub() function uses sys._getframe(1) to return the stack frame of the caller. From
that, the f_locals attribute is accessed to get the local variables. It goes without saying
that messing around with stack frames should probably be avoided in most code. How‐
ever, for utility functions such as a string substitution feature, it can be useful. As an
aside, it’s probably worth noting that f_locals is a dictionary that is a copy of the local
variables in the calling function. Although you can modify the contents of f_locals,
```
[^35]
**Annotation:** This excerpt demonstrates 'debugging' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 3: Numbers, Dates, and Times** *(pp.83–112)*

This later chapter builds upon the concepts introduced here, particularly: None, argument, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^36]

**Annotation:** Forward reference: Chapter 3 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, argument appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 4: Iterators and Generators** *(pp.113–140)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __repr__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^37]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Files and I/O** *(pp.141–174)*

This later chapter builds upon the concepts introduced here, particularly: None, argument, as.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^38]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, argument appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 3: Numbers, Dates, and Times

*Source: Python Cookbook, 3rd Edition, pages 83–112*

### Chapter Summary
This chapter covers numbers, dates, and times. Key topics include string, function, and module. Covers string, method, file. [^39]

### Concept-by-Concept Breakdown
#### **None** *(p.89)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.89, lines 15–22)*:
```
    scanner = master_pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok
# Parser
class ExpressionEvaluator:
    '''
```
[^40]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.98)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.98, lines 34–41)*:
```
decoding. For example:
>>> # Write a UTF-8 filename
>>> with open('jalape\xf1o.txt', 'w') as f:
...     f.write('spicy')
...
>>> # Get a directory listing
>>> import os
>>> os.listdir('.')          # Text string (names are decoded)
```
[^41]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.83)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.83, lines 30–37)*:
```
If you’re trying to emit text as ASCII and want to embed character code entities for non-
ASCII characters, you can use the errors='xmlcharrefreplace' argument to various
I/O-related functions to do it. For example:
>>> s = 'Spicy Jalapeño'
>>> s.encode('ascii', errors='xmlcharrefreplace')
b'Spicy Jalape&#241;o'
>>>
2.17. Handling HTML and XML Entities in Text 
```
[^42]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.97)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.97, lines 10–17)*:
```
>>>
Such operations also work with byte arrays. For example:
>>> data = bytearray(b'Hello World')
>>> data[0:5]
bytearray(b'Hello')
>>> data.startswith(b'Hello')
True
>>> data.split()
```
[^43]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.83)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.83, lines 8–15)*:
```
>>>
The fill() method has a few additional options that control how it handles tabs, sen‐
tence endings, and so on. Look at the documentation for the textwrap.TextWrapper
class for further details.
2.17. Handling HTML and XML Entities in Text
Problem
You want to replace HTML or XML entities such as &entity; or &#code; with their
corresponding text. Alternatively, you need to produce text, but escape certain charac‐
```
[^44]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 13 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.98)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.98, lines 23–30)*:
```
  File "<stdin>", line 1, in <module>
AttributeError: 'bytes' object has no attribute 'format'
>>>
If you want to do any kind of formatting applied to byte strings, it should be done using
normal text strings and encoding. For example:
>>> '{:10s} {:10d} {:10.2f}'.format('ACME', 100, 490.1).encode('ascii')
b'ACME              100     490.10'
>>>
```
[^45]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.91)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.91, lines 24–31)*:
```
If you want to do something other than pure evaluation, you need to change the
ExpressionEvaluator class to do something else. For example, here is an alternative
implementation that constructs a simple parse tree:
class ExpressionTreeBuilder(ExpressionEvaluator):
    def expr(self):
        "expression ::= term { ('+'|'-') term }"
        exprval = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
```
[^46]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.88)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.88, lines 4–11)*:
```
           |   NUM
In an EBNF, parts of a rule enclosed in { ... }* are optional. The * means zero or more
repetitions (the same meaning as in a regular expression).
Now, if you’re not familiar with the mechanics of working with a BNF, think of it as a
specification of substitution or replacement rules where symbols on the left side can be
replaced by the symbols on the right (or vice versa). Generally, what happens during
parsing is that you try to match the input text to the grammar by making various sub‐
stitutions and expansions using the BNF. To illustrate, suppose you are parsing an ex‐
```
[^47]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.86)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.86, lines 2–9)*:
```
into a generator like this:
from collections import namedtuple
Token = namedtuple('Token', ['type','value'])
def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())
# Example use
```
[^48]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.95)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.95, lines 2–9)*:
```
# Token processing functions
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t
# Error handler
def t_error(t):
    print('Bad character: {!r}'.format(t.value[0]))
```
[^49]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Elif** *(p.90)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.90, lines 13–20)*:
```
                exprval += right
            elif op == 'MINUS':
                exprval -= right
        return exprval
    def term(self):
        "term ::= factor { ('*'|'/') factor }*"
        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
```
[^50]
**Annotation:** This excerpt demonstrates 'elif' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Else** *(p.89)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.89, lines 42–47)*:
```
            return True
        else:
            return False
2.19. Writing a Simple Recursive Descent Parser 
| 
71
```
[^51]
**Annotation:** This excerpt demonstrates 'else' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Encoding** *(p.98)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.98, lines 26–33)*:
```
If you want to do any kind of formatting applied to byte strings, it should be done using
normal text strings and encoding. For example:
>>> '{:10s} {:10d} {:10.2f}'.format('ACME', 100, 490.1).encode('ascii')
b'ACME              100     490.10'
>>>
Finally, you need to be aware that using a byte string can change the semantics of certain
operations—especially those related to the filesystem. For example, if you supply a file‐
name encoded as bytes instead of a text string, it usually disables filename encoding/
```
[^52]
**Annotation:** This excerpt demonstrates 'encoding' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **File** *(p.91)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.91, lines 6–13)*:
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "exprparse.py", line 40, in parse
    return self.expr()
  File "exprparse.py", line 67, in expr
    right = self.term()
  File "exprparse.py", line 77, in term
    termval = self.factor()
```
[^53]
**Annotation:** This excerpt demonstrates 'file' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Finally** *(p.98)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.98, lines 30–37)*:
```
>>>
Finally, you need to be aware that using a byte string can change the semantics of certain
operations—especially those related to the filesystem. For example, if you supply a file‐
name encoded as bytes instead of a text string, it usually disables filename encoding/
decoding. For example:
>>> # Write a UTF-8 filename
>>> with open('jalape\xf1o.txt', 'w') as f:
...     f.write('spicy')
```
[^54]
**Annotation:** This excerpt demonstrates 'finally' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 4: Iterators and Generators** *(pp.113–140)*

This later chapter builds upon the concepts introduced here, particularly: None, argument, array.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^55]

**Annotation:** Forward reference: Chapter 4 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, argument appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 5: Files and I/O** *(pp.141–174)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^56]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Data Encoding and Processing** *(pp.175–216)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^57]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 4: Iterators and Generators

*Source: Python Cookbook, 3rd Edition, pages 113–140*

### Chapter Summary
This chapter covers iterators and generators. Key topics include functions, generator, and iterators. Covers function, iterator, generator. [^58]

### Concept-by-Concept Breakdown
#### **None** *(p.137)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.137, lines 5–12)*:
```
        self._node = start_node
        self._children_iter = None
        self._child_iter = None
    def __iter__(self):
        return self
    def __next__(self):
        # Return myself if just started; create an iterator for children
        if self._children_iter is None:
```
[^59]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.133)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.133, lines 1–8)*:
```
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []
    def __repr__(self):
        return 'Node({!r})'.format(self._value)
    def add_child(self, node):
        self._children.append(node)
```
[^60]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.133)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.133, lines 11–18)*:
```
# Example
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
```
[^61]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.133)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.133, lines 11–18)*:
```
# Example
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
```
[^62]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Repr__** *(p.133)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.133, lines 4–11)*:
```
        self._children = []
    def __repr__(self):
        return 'Node({!r})'.format(self._value)
    def add_child(self, node):
        self._children.append(node)
    def __iter__(self):
        return iter(self._children)
# Example
```
[^63]
**Annotation:** This excerpt demonstrates '__repr__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.123)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.123, lines 23–30)*:
```
  File "<stdin>", line 1, in <module>
TypeError: 'months' is an invalid keyword argument for this function
>>>
>>> from dateutil.relativedelta import relativedelta
>>> a + relativedelta(months=+1)
datetime.datetime(2012, 10, 23, 0, 0)
>>> a + relativedelta(months=+4)
datetime.datetime(2013, 1, 23, 0, 0)
```
[^64]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.115)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.115, lines 1–8)*:
```
3.9. Calculating with Large Numerical Arrays
Problem
You need to perform calculations on large numerical datasets, such as arrays or grids.
Solution
For any heavy computation involving arrays, use the NumPy library. The major feature
of NumPy is that it gives Python an array object that is much more efficient and better
suited for mathematical calculation than a standard Python list. Here is a short example
illustrating important behavioral differences between lists and NumPy arrays:
```
[^65]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 17 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.139)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.139, lines 1–8)*:
```
Solution
If you want a generator to expose extra state to the user, don’t forget that you can easily
implement it as a class, putting the generator function code in the __iter__() method.
For example:
from collections import deque
class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
```
[^66]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 14 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.139)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.139, lines 16–23)*:
```
To use this class, you would treat it like a normal generator function. However, since it
creates an instance, you can access internal attributes, such as the history attribute or
the clear() method. For example:
with open('somefile.txt') as f:
     lines = linehistory(f)
     for line in lines:
         if 'python' in line:
             for lineno, hline in lines.history:
```
[^67]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.132)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.132, lines 4–11)*:
```
         if line is None:
             break
         print(line, end='')
Discussion
In most cases, the for statement is used to consume an iterable. However, every now
and then, a problem calls for more precise control over the underlying iteration mech‐
anism. Thus, it is useful to know what actually happens.
The following interactive example illustrates the basic mechanics of what happens dur‐
```
[^68]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.139)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.139, lines 2–9)*:
```
If you want a generator to expose extra state to the user, don’t forget that you can easily
implement it as a class, putting the generator function code in the __iter__() method.
For example:
from collections import deque
class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)
```
[^69]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.139)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.139, lines 4–11)*:
```
For example:
from collections import deque
class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)
    def __iter__(self):
        for lineno, line in enumerate(self.lines,1):
```
[^70]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Datetime** *(p.124)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.124, lines 5–12)*:
```
Solution
Python’s datetime module has utility functions and classes to help perform calculations
like this. A decent, generic solution to this problem looks like this:
from datetime import datetime, timedelta
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']
def get_previous_byday(dayname, start_date=None):
    if start_date is None:
```
[^71]
**Annotation:** This excerpt demonstrates 'datetime' as it appears in the primary text. The concept occurs 17 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.138)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.138, lines 15–22)*:
```
Many programmers don’t realize that reversed iteration can be customized on user-
defined classes if they implement the __reversed__() method. For example:
class Countdown:
    def __init__(self, start):
        self.start = start
    # Forward iterator
    def __iter__(self):
        n = self.start
```
[^72]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Dictionary** *(p.130)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.130, lines 17–24)*:
```
time zone name for India? To find out, you can consult the pytz.country_timezones
dictionary using the ISO 3166 country code as a key. For example:
>>> pytz.country_timezones['IN']
['Asia/Kolkata']
>>>
By the time you read this, it’s possible that the pytz module will be
deprecated in favor of improved time zone support, as described in PEP
431. Many of the same issues will still apply, however (e.g., advice using
```
[^73]
**Annotation:** This excerpt demonstrates 'dictionary' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 5: Files and I/O** *(pp.141–174)*

This later chapter builds upon the concepts introduced here, particularly: None, argument, array.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^74]

**Annotation:** Forward reference: Chapter 5 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, argument appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 6: Data Encoding and Processing** *(pp.175–216)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^75]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Functions** *(pp.217–242)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^76]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 5: Files and I/O

*Source: Python Cookbook, 3rd Edition, pages 141–174*

### Chapter Summary
This chapter covers files and i/o. Key topics include functions, iterators, and generators. Covers file, function, generator. [^77]

### Concept-by-Concept Breakdown
#### **None** *(p.142)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.142, lines 14–21)*:
```
>>> items = ['a', 'b', 'c', 1, 4, 10, 15]
>>> for x in islice(items, 3, None):
...     print(x)
...
1
4
10
15
```
[^78]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.160)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.160, lines 9–16)*:
```
By default, files are read/written using the system default text encoding, as can be found
in sys.getdefaultencoding(). On most machines, this is set to utf-8. If you know
that the text you are reading or writing is in a different encoding, supply the optional
encoding parameter to open(). For example:
with open('somefile.txt', 'rt', encoding='latin-1') as f:
     ...
Python understands several hundred possible text encodings. However, some of the
more common encodings are ascii, latin-1, utf-8, and utf-16. UTF-8 is usually a
```
[^79]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.162)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.162, lines 1–8)*:
```
If you’re constantly fiddling with the encoding and errors arguments to open() and
doing lots of hacks, you’re probably making life more difficult than it needs to be. The
number one rule with text is that you simply need to make sure you’re always using the
proper text encoding. When in doubt, use the default setting (typically UTF-8).
5.2. Printing to a File
Problem
You want to redirect the output of the print() function to a file.
Solution
```
[^80]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.165)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.165, lines 8–15)*:
```
    f.write(text.encode('utf-8'))
A lesser-known aspect of binary I/O is that objects such as arrays and C structures can
be used for writing without any kind of intermediate conversion to a bytes object. For
example:
import array
nums = array.array('i', [1, 2, 3, 4])
with open('data.bin','wb') as f:
    f.write(nums)
```
[^81]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.152)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.152, lines 19–26)*:
```
including parsing, reading from real-time data sources, periodic polling, and so on.
In understanding the code, it is important to grasp that the yield statement acts as a
kind of data producer whereas a for loop acts as a data consumer. When the generators
are stacked together, each yield feeds a single item of data to the next stage of the
pipeline that is consuming it with iteration. In the last example, the sum() function is
actually driving the entire program, pulling one item at a time out of the pipeline of
generators.
One nice feature of this approach is that each generator function tends to be small and
```
[^82]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 13 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Binary Mode** *(p.162)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.162, lines 13–20)*:
```
There’s not much more to printing to a file other than this. However, make sure that the
file is opened in text mode. Printing will fail if the underlying file is in binary mode.
5.3. Printing with a Different Separator or Line Ending
Problem
You want to output data using print(), but you also want to change the separator
character or line ending.
Solution
Use the sep and end keyword arguments to print() to change the output as you wish.
```
[^83]
**Annotation:** This excerpt demonstrates 'binary mode' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.142)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.142, lines 33–40)*:
```
        if not line.startswith('#'):
            break
    # Process remaining lines
    while line:
        # Replace with useful processing
        print(line, end='')
        line = next(f, None)
Discarding the first part of an iterable is also slightly different than simply filtering all
```
[^84]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.167)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.167, lines 1–8)*:
```
Solution
Use the io.StringIO() and io.BytesIO() classes to create file-like objects that operate
on string data. For example:
>>> s = io.StringIO()
>>> s.write('Hello World\n')
12
>>> print('This is a test', file=s)
15
```
[^85]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.160)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.160, lines 27–34)*:
```
examples establishes a context in which the file will be used. When control leaves the
with block, the file will be closed automatically. You don’t need to use the with statement,
but if you don’t use it, make sure you remember to close the file:
f = open('somefile.txt', 'rt')
data = f.read()
f.close()
Another minor complication concerns the recognition of newlines, which are different
on Unix and Windows (i.e., \n versus \r\n). By default, Python operates in what’s known
```
[^86]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.153)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.153, lines 18–25)*:
```
statement. For example:
from collections import Iterable
def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x
```
[^87]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Context Manager** *(p.172)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.172, lines 31–38)*:
```
>>>
The mmap object returned by mmap() can also be used as a context manager, in which
case the underlying file is closed automatically. For example:
>>> with memory_map('data') as m:
...      print(len(m))
...      print(m[0:10])
...
1000000
```
[^88]
**Annotation:** This excerpt demonstrates 'context manager' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Coroutine** *(p.154)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.154, lines 28–35)*:
```
Finally, it should be noted that yield from has a more important role in advanced
programs involving coroutines and generator-based concurrency. See Recipe 12.12 for
another example.
4.15. Iterating in Sorted Order Over Merged Sorted
Iterables
Problem
You have a collection of sorted sequences and you want to iterate over a sorted sequence
of them all merged together.
```
[^89]
**Annotation:** This excerpt demonstrates 'coroutine' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Csv** *(p.174)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.174, lines 10–17)*:
```
>>> import os
>>> path = '/Users/beazley/Data/data.csv'
>>> # Get the last component of the path
>>> os.path.basename(path)
'data.csv'
>>> # Get the directory name
>>> os.path.dirname(path)
'/Users/beazley/Data'
```
[^90]
**Annotation:** This excerpt demonstrates 'csv' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Def** *(p.151)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.151, lines 2–9)*:
```
    ...
To process these files, you could define a collection of small generator functions that
perform specific self-contained tasks. For example:
import os
import fnmatch
import gzip
import bz2
import re
```
[^91]
**Annotation:** This excerpt demonstrates 'def' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Descriptor** *(p.167)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.167, lines 32–39)*:
```
Be aware that StringIO and BytesIO instances don’t have a proper integer file-
descriptor. Thus, they do not work with code that requires the use of a real system-level
file such as a file, pipe, or socket.
5.7. Reading and Writing Compressed Datafiles
Problem
You need to read or write data in a file with gzip or bz2 compression.
5.7. Reading and Writing Compressed Datafiles 
| 
```
[^92]
**Annotation:** This excerpt demonstrates 'descriptor' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 6: Data Encoding and Processing** *(pp.175–216)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^93]

**Annotation:** Forward reference: Chapter 6 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 7: Functions** *(pp.217–242)*

This later chapter builds upon the concepts introduced here, particularly: None, argument, array.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^94]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, argument appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Classes and Objects** *(pp.243–328)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, argument.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^95]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 6: Data Encoding and Processing

*Source: Python Cookbook, 3rd Edition, pages 175–216*

### Chapter Summary
This chapter covers data encoding and processing. Key topics include encoding, json. Covers file, function. [^96]

### Concept-by-Concept Breakdown
#### **None** *(p.198)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.198, lines 4–11)*:
```
minor changes. For instance, True is mapped to true, False is mapped to false, and
None is mapped to null. Here is an example that shows what the encoding looks like:
>>> json.dumps(False)
'false'
>>> d = {'a': True,
...      'b': 'Hello',
...      'c': None}
>>> json.dumps(d)
```
[^97]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.182)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.182, lines 2–9)*:
```
>>> f
<_io.TextIOWrapper name='sample.txt' mode='w' encoding='UTF-8'>
>>> f.buffer
<_io.BufferedWriter name='sample.txt'>
>>> f.buffer.raw
<_io.FileIO name='sample.txt' mode='wb'>
>>>
In this example, io.TextIOWrapper is a text-handling layer that encodes and decodes
```
[^98]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.200)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.200, lines 6–13)*:
```
>>> class Point:
...     def __init__(self, x, y):
...             self.x = x
...             self.y = y
...
>>> p = Point(2, 3)
>>> json.dumps(p)
Traceback (most recent call last):
```
[^99]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.200)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.200, lines 22–29)*:
```
    raise TypeError(repr(o) + " is not JSON serializable")
TypeError: <__main__.Point object at 0x1006f2650> is not JSON serializable
>>>
If you want to serialize instances, you can supply a function that takes an instance as
input and returns a dictionary that can be serialized. For example:
def serialize_instance(obj):
    d = { '__classname__' : type(obj).__name__ }
    d.update(vars(obj))
```
[^100]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.200)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.200, lines 27–34)*:
```
def serialize_instance(obj):
    d = { '__classname__' : type(obj).__name__ }
    d.update(vars(obj))
    return d
If you want to get an instance back, you could write code like this:
# Dictionary mapping names to known classes
classes = {
    'Point' : Point
```
[^101]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.212)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.212, lines 16–23)*:
```
class XMLNamespaces:
    def __init__(self, **kwargs):
        self.namespaces = {}
        for name, uri in kwargs.items():
            self.register(name, uri)
    def register(self, name, uri):
        self.namespaces[name] = '{'+uri+'}'
    def __call__(self, path):
```
[^102]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.186)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.186, lines 18–25)*:
```
# File is destroyed
The first argument to TemporaryFile() is the file mode, which is usually w+t for text
and w+b for binary. This mode simultaneously supports reading and writing, which is
useful here since closing the file to change modes would actually destroy it. Temporary
File() additionally accepts the same arguments as the built-in open() function. For
example:
with TemporaryFile('w+t', encoding='utf-8', errors='ignore') as f:
     ...
```
[^103]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.191)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.191, lines 37–44)*:
```
pickle is not a particularly efficient encoding for large data structures such as binary
arrays created by libraries like the array module or numpy. If you’re moving large
amounts of array data around, you may be better off simply saving bulk array data in a
file or using a more standardized encoding, such as HDF5 (supported by third-party
libraries).
5.21. Serializing Python Objects 
| 
173
```
[^104]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.215)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.215, lines 1–8)*:
```
Discussion
At a low level, interacting with a database is an extremely straightforward thing to do.
You simply form SQL statements and feed them to the underlying module to either
update the database or retrieve data. That said, there are still some tricky details you’ll
need to sort out on a case-by-case basis.
One complication is the mapping of data from the database into Python types. For
entries such as dates, it is most common to use datetime instances from the date
time module, or possibly system timestamps, as used in the time module. For numerical
```
[^105]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 26 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.203)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.203, lines 26–33)*:
```
calls to item.findtext() take place relative to the found “item” elements.
Each element represented by the ElementTree module has a few essential attributes and
methods that are useful when parsing. The tag attribute contains the name of the tag,
the text attribute contains enclosed text, and the get() method can be used to extract
attributes (if any). For example:
>>> doc
<xml.etree.ElementTree.ElementTree object at 0x101339510>
>>> e = doc.find('channel/title')
```
[^106]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Binary Mode** *(p.181)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.181, lines 15–22)*:
```
If you want to add Unicode encoding/decoding to an already existing file object that’s
opened in binary mode, wrap it with an io.TextIOWrapper() object. For example:
import urllib.request
import io
u = urllib.request.urlopen('http://www.python.org')
f = io.TextIOWrapper(u,encoding='utf-8')
text = f.read()
If you want to change the encoding of an already open text-mode file, use its detach()
```
[^107]
**Annotation:** This excerpt demonstrates 'binary mode' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.179)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.179, lines 1–8)*:
```
conform to the expected encoding rules. Such filenames may mysteriously break Python
programs that work with a lot of files.
Reading directories and working with filenames as raw undecoded bytes has the po‐
tential to avoid such problems, albeit at the cost of programming convenience.
See Recipe 5.15 for a recipe on printing undecodable filenames.
5.15. Printing Bad Filenames
Problem
Your program received a directory listing, but when it tried to print the filenames, it
```
[^108]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.200)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.200, lines 5–12)*:
```
Instances are not normally serializable as JSON. For example:
>>> class Point:
...     def __init__(self, x, y):
...             self.x = x
...             self.y = y
...
>>> p = Point(2, 3)
>>> json.dumps(p)
```
[^109]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.184)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.184, lines 17–24)*:
```
f.write('hello world\n')
f.close()
When the high-level file object is closed or destroyed, the underlying file descriptor will
also be closed. If this is not desired, supply the optional closefd=False argument to
open(). For example:
# Create a file object, but don't close underlying fd when done
f = open(fd, 'wt', closefd=False)
...
```
[^110]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.194)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.194, lines 6–13)*:
```
consider the use of named tuples. For example:
from collections import namedtuple
with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for r in f_csv:
        row = Row(*r)
```
[^111]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 7: Functions** *(pp.217–242)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^112]

**Annotation:** Forward reference: Chapter 7 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 8: Classes and Objects** *(pp.243–328)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^113]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Metaprogramming** *(pp.329–396)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^114]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 7: Functions

*Source: Python Cookbook, 3rd Edition, pages 217–242*

### Chapter Summary
This chapter covers functions. Key topics include functions, object, and encoding. Covers function, class, file. [^115]

### Concept-by-Concept Breakdown
#### **None** *(p.240)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.240, lines 14–21)*:
```
If the default value is supposed to be a mutable container, such as a list, set, or dictionary,
use None as the default and write code like this:
# Using a list as a default value
def spam(a, b=None):
    if b is None:
        b = []
    ...
If, instead of providing a default value, you want to write code that merely tests whether
```
[^116]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.224)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.224, lines 5–12)*:
```
    '''
    def __init__(self, format, offset):
        self.format = format
        self.offset = offset
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
```
[^117]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.229)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.229, lines 7–14)*:
```
>>> polydata
[<__main__.SizedRecord object at 0x1006a4d50>,
 <__main__.SizedRecord object at 0x1006a4f50>,
 <__main__.SizedRecord object at 0x10070da90>]
>>>
As shown, the contents of the SizedRecord instances have not yet been interpreted. To
do that, use the iter_as() method, which accepts a structure format code or Struc
ture class as input. This gives you a lot of flexibility in how to interpret the data. For
```
[^118]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.218)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.218, lines 13–20)*:
```
# Example
if __name__ == '__main__':
    records = [ (1, 2.3, 4.5),
                (6, 7.8, 9.0),
                (12, 13.4, 56.7) ]
    with open('data.b', 'wb') as f:
         write_records(records, '<idd', f)
There are several approaches for reading this file back into a list of tuples. First, if you’re
```
[^119]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Annotation** *(p.238)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.238, lines 11–18)*:
```
Solution
Function argument annotations can be a useful way to give programmers hints about
how a function is supposed to be used. For example, consider the following annotated
function:
def add(x:int, y:int) -> int:
    return x + y
The Python interpreter does not attach any semantic meaning to the attached annota‐
tions. They are not type checks, nor do they make Python behave any differently than
```
[^120]
**Annotation:** This excerpt demonstrates 'annotation' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.236)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.236, lines 19–26)*:
```
arguments, use * and ** together. For example:
def anyargs(*args, **kwargs):
    print(args)      # A tuple
    print(kwargs)    # A dict
With this function, all of the positional arguments are placed into a tuple args, and all
of the keyword arguments are placed into a dictionary kwargs.
Discussion
A * argument can only appear as the last positional argument in a function definition.
```
[^121]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 10 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.236)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.236, lines 1–8)*:
```
To accept any number of keyword arguments, use an argument that starts with **. For
example:
import html
def make_element(name, value, **attrs):
    keyvals = [' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(
                  name=name,
```
[^122]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 14 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.217)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.217, lines 19–26)*:
```
Base64 encoding is only meant to be used on byte-oriented data such as byte strings and
byte arrays. Moreover, the output of the encoding process is always a byte string. If you
are mixing Base64-encoded data with Unicode text, you may have to perform an extra
decoding step. For example:
>>> a = base64.b64encode(s).decode('ascii')
>>> a
'aGVsbG8='
>>>
```
[^123]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.217)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.217, lines 1–8)*:
```
6.10. Decoding and Encoding Base64
Problem
You need to decode or encode binary data using Base64 encoding.
Solution
The base64 module has two functions—b64encode() and b64decode()—that do ex‐
actly what you want. For example:
>>> # Some byte data
>>> s = b'hello'
```
[^124]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 19 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.219)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.219, lines 19–26)*:
```
character to > for big endian or ! for network byte order.
The resulting Struct instance has various attributes and methods for manipulating
structures of that type. The size attribute contains the size of the structure in bytes,
which is useful to have in I/O operations. pack() and unpack() methods are used to
pack and unpack data. For example:
>>> from struct import Struct
>>> record_struct = Struct('<idd')
>>> record_struct.size
```
[^125]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.220)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.220, lines 29–36)*:
```
        if chk == b'':
            break
        yield record_struct.unpack(chk)
    return records
In the unpack_records() function, a different approach using the unpack_from()
method is used. unpack_from() is a useful method for extracting binary data from a
larger binary array, because it does so without making any temporary objects or memory
copies. You just give it a byte string (or any array) along with a byte offset, and it will
```
[^126]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.225)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.225, lines 8–15)*:
```
This is interesting, but there are a number of annoyances with this approach. For one,
even though you get the convenience of a class-like interface, the code is rather verbose
and requires the user to specify a lot of low-level detail (e.g., repeated uses of Struct
Field, specification of offsets, etc.). The resulting class is also missing common con‐
veniences such as providing a way to compute the total size of the structure.
Any time you are faced with class definitions that are overly verbose like this, you might
consider the use of a class decorator or metaclass. One of the features of a metaclass is
that it can be used to fill in a lot of low-level implementation details, taking that burden
```
[^127]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 15 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class Method** *(p.228)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.228, lines 36–43)*:
```
                yield code(data)
The SizedRecord.from_file() class method is a utility for reading a size-prefixed
chunk of data from a file, which is common in many file formats. As input, it accepts a
structure format code containing the encoding of the size, which is expected to be in
bytes. The optional includes_size argument specifies whether the number of bytes
includes the size header or not. Here’s an example of how you would use this code to
read the individual polygons in the polygon file:
210 
```
[^128]
**Annotation:** This excerpt demonstrates 'class method' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.228)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.228, lines 14–21)*:
```
One way to handle this is to write a class that simply represents a chunk of binary data
along with a utility function for interpreting the contents in different ways. This is closely
related to the code in Recipe 6.11:
class SizedRecord:
    def __init__(self, bytedata):
        self._buffer = memoryview(bytedata)
    @classmethod
    def from_file(cls, f, size_fmt, includes_size=True):
```
[^129]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Closure** *(p.235)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.235, lines 5–12)*:
```
usage patterns. Topics include default arguments, functions that take any number of
arguments, keyword-only arguments, annotations, and closures. In addition, some
tricky control flow and data passing problems involving callback functions are
addressed.
7.1. Writing Functions That Accept Any Number of
Arguments
Problem
You want to write a function that accepts any number of input arguments.
```
[^130]
**Annotation:** This excerpt demonstrates 'closure' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 8: Classes and Objects** *(pp.243–328)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^131]

**Annotation:** Forward reference: Chapter 8 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 9: Metaprogramming** *(pp.329–396)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^132]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: Modules and Packages** *(pp.397–436)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^133]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 8: Classes and Objects

*Source: Python Cookbook, 3rd Edition, pages 243–328*

### Chapter Summary
This chapter covers classes and objects. Key topics include functions, classes, and object. Covers class, method, function. [^134]

### Concept-by-Concept Breakdown
#### **Gil** *(p.268)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.268, lines 21–28)*:
```
Python doesn’t actually prevent someone from accessing internal names. However, do‐
ing so is considered impolite, and may result in fragile code. It should be noted, too,
that the use of the leading underscore is also used for module names and module-level
functions. For example, if you ever see a module name that starts with a leading un‐
derscore (e.g., _socket), it’s internal implementation. Likewise, module-level functions
such as sys._getframe() should only be used with great caution.
You may also encounter the use of two leading underscores (__) on names within class
definitions. For example:
```
[^135]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Mro** *(p.276)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.276, lines 30–37)*:
```
implements inheritance. For every class that you define, Python computes what’s known
as a method resolution order (MRO) list. The MRO list is simply a linear ordering of
all the base classes. For example:
>>> C.__mro__
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>,
<class '__main__.Base'>, <class 'object'>)
>>>
To implement inheritance, Python starts with the leftmost class and works its way left-
```
[^136]
**Annotation:** This excerpt demonstrates 'MRO' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.284)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.284, lines 10–17)*:
```
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]
    ...
The reason __get__() looks somewhat complicated is to account for the distinction
between instance variables and class variables. If a descriptor is accessed as a class vari‐
```
[^137]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.249)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.249, lines 17–24)*:
```
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))
The class could be replaced with a much simpler function:
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener
# Example use
```
[^138]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.265)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.265, lines 8–15)*:
```
with conn as s:
    # conn.__enter__() executes: connection open
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # conn.__exit__() executes: connection closed
Discussion
```
[^139]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.265)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.265, lines 13–20)*:
```
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # conn.__exit__() executes: connection closed
Discussion
The main principle behind writing a context manager is that you’re writing code that’s
meant to surround a block of statements as defined by the use of the with statement.
When the with statement is first encountered, the __enter__() method is triggered.
The return value of __enter__() (if any) is placed into the variable indicated with the
as qualifier. Afterward, the statements in the body of the with statement execute. Finally,
```
[^140]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.275)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.275, lines 10–17)*:
```
class Base:
    def __init__(self):
        print('Base.__init__')
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')
Although this “works” for most code, it can lead to bizarre trouble in advanced code
```
[^141]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 21 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.276)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.276, lines 33–40)*:
```
>>> C.__mro__
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>,
<class '__main__.Base'>, <class 'object'>)
>>>
To implement inheritance, Python starts with the leftmost class and works its way left-
to-right through classes on the MRO list until it finds the first attribute match.
The actual determination of the MRO list itself is made using a technique known as C3
Linearization. Without getting too bogged down in the mathematics of it, it is actually
```
[^142]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.289)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.289, lines 1–8)*:
```
# Example class definitions
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']
    class Point(Structure):
        _fields = ['x','y']
    class Circle(Structure):
        _fields = ['radius']
```
[^143]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Repr__** *(p.262)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.262, lines 2–9)*:
```
>>> p
Pair(3, 4)         # __repr__() output
>>> print(p)
(3, 4)             # __str__() output
>>>
The implementation of this recipe also shows how different string representations may
be used during formatting. Specifically, the special !r formatting code indicates that the
output of __repr__() should be used instead of __str__(), the default. You can try this
```
[^144]
**Annotation:** This excerpt demonstrates '__repr__' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Str__** *(p.262)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.262, lines 4–11)*:
```
>>> print(p)
(3, 4)             # __str__() output
>>>
The implementation of this recipe also shows how different string representations may
be used during formatting. Specifically, the special !r formatting code indicates that the
output of __repr__() should be used instead of __str__(), the default. You can try this
experiment with the preceding class to see this:
>>> p = Pair(3, 4)
```
[^145]
**Annotation:** This excerpt demonstrates '__str__' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.248)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.248, lines 1–8)*:
```
class EchoHandler(StreamRequestHandler):
    # ack is added keyword-only argument. *args, **kwargs are
    # any normal parameters supplied (which are passed on)
    def __init__(self, *args, ack, **kwargs):
        self.ack = ack
        super().__init__(*args, **kwargs)
    def handle(self):
        for line in self.rfile:
```
[^146]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 10 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.289)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.289, lines 18–25)*:
```
  File "structure.py", line 6, in __init__
    raise TypeError('Expected {} arguments'.format(len(self._fields)))
TypeError: Expected 3 arguments
Should you decide to support keyword arguments, there are several design options. One
choice is to map the keyword arguments so that they only correspond to the attribute
names specified in _fields. For example:
class Structure:
    _fields= []
```
[^147]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.267)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.267, lines 12–19)*:
```
for instances. Instead of each instance consisting of a dictionary, instances are built
around a small fixed-sized array, much like a tuple or list. Attribute names listed in the
__slots__ specifier are internally mapped to specific indices within this array. A side
effect of using slots is that it is no longer possible to add new attributes to instances—
you are restricted to only those attribute names listed in the __slots__ specifier.
Discussion
The memory saved by using slots varies according to the number and type of attributes
stored. However, in general, the resulting memory use is comparable to that of storing
```
[^148]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.292)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.292, lines 1–8)*:
```
class Stock:
    def __init__(self, name, shares, price):
        init_fromlocals(self)
In this variation, the init_fromlocals() function uses sys._getframe() to peek at the
local variables of the calling method. If used as the first step of an __init__() method,
the local variables will be the same as the passed arguments and can be easily used to
set attributes with the same names. Although this approach avoids the problem of get‐
ting the right calling signature in IDEs, it runs more than 50% slower than the solution
```
[^149]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 29 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 9: Metaprogramming** *(pp.329–396)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^150]

**Annotation:** Forward reference: Chapter 9 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 10: Modules and Packages** *(pp.397–436)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, UTF-8.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^151]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Network and Web Programming** *(pp.437–484)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^152]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 9: Metaprogramming

*Source: Python Cookbook, 3rd Edition, pages 329–396*

### Chapter Summary
In
addition to allowing traversal of tree structures, it provides a variation that allows a data
structure to be rewritten or transformed as it is traversed (e.g., nodes added or removed) Key topics include decorator, functions, and objects. Covers class, method, decorator. [^153]

### Concept-by-Concept Breakdown
#### **None** *(p.336)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.336, lines 4–11)*:
```
        self.value = value
        self._parent = None
        self.children = []
    def __repr__(self):
        return 'Node({!r:})'.format(self.value)
    # property that manages the parent as a weak-reference
    @property
    def parent(self):
```
[^154]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Eq__** *(p.340)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.340, lines 1–8)*:
```
def __eq__(self, other):
        return self.living_space_footage == other.living_space_footage
    def __lt__(self, other):
        return self.living_space_footage < other.living_space_footage
Here, the House class has been decorated with @total_ordering. Definitions of
__eq__() and __lt__() are provided to compare houses based on the total square
footage of their rooms. This minimum definition is all that is required to make all of
the other comparison operations work. For example:
```
[^155]
**Annotation:** This excerpt demonstrates '__eq__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.381)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.381, lines 1–8)*:
```
To support such keyword arguments in a metaclass, make sure you define them on the
__prepare__(), __new__(), and __init__() methods using keyword-only arguments,
like this:
class MyMeta(type):
    # Optional
    @classmethod
    def __prepare__(cls, name, bases, *, debug=False, synchronize=False):
        # Custom processing
```
[^156]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.355)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.355, lines 23–30)*:
```
>>> add(2, 3)
DEBUG:__main__:add
5
>>> # Change the log message
>>> add.set_message('Add called')
>>> add(2, 3)
DEBUG:__main__:Add called
5
```
[^157]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.350)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.350, lines 3–10)*:
```
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper
Here is an example of using the decorator and examining the resulting function meta‐
data:
>>> @timethis
... def countdown(n:int):
```
[^158]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Repr__** *(p.336)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.336, lines 6–13)*:
```
        self.children = []
    def __repr__(self):
        return 'Node({!r:})'.format(self.value)
    # property that manages the parent as a weak-reference
    @property
    def parent(self):
        return self._parent if self._parent is None else self._parent()
    @parent.setter
```
[^159]
**Annotation:** This excerpt demonstrates '__repr__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Str__** *(p.339)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.339, lines 33–40)*:
```
        self.rooms.append(room)
    def __str__(self):
        return '{}: {} square foot {}'.format(self.name,
                                              self.living_space_footage,
                                              self.style)
8.24. Making Classes Support Comparison Operations 
| 
321
```
[^160]
**Annotation:** This excerpt demonstrates '__str__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Annotation** *(p.363)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.363, lines 3–10)*:
```
    print(x,y,z)
One possible reason for not using annotations is that each argument to a function can
only have a single annotation assigned. Thus, if the annotations are used for type as‐
sertions, they can’t really be used for anything else. Likewise, the @typeassert decorator
won’t work with functions that use annotations for a different purpose. By using deco‐
rator arguments, as shown in the solution, the decorator becomes a lot more general
purpose and can be used with any function whatsoever—even functions that use
annotations.
```
[^161]
**Annotation:** This excerpt demonstrates 'annotation' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.360)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.360, lines 6–13)*:
```
from functools import wraps
def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func
        # Map function argument names to supplied types
        sig = signature(func)
```
[^162]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 10 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.362)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.362, lines 2–9)*:
```
>>>
In this partial binding, you will notice that missing arguments are simply ignored (i.e.,
there is no binding for argument y). However, the most important part of the binding
is the creation of the ordered dictionary bound_types.arguments. This dictionary maps
the argument names to the supplied values in the same order as the function signature.
In the case of our decorator, this mapping contains the type assertions that we’re going
to enforce.
In the actual wrapper function made by the decorator, the sig.bind() method is used.
```
[^163]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 12 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.386)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.386, lines 1–8)*:
```
# bases is tuple of base classes
        # clsdict is class dictionary
To use a metaclass, you would generally incorporate it into a top-level base class from
which other objects inherit. For example:
class Root(metaclass=MyMeta):
    pass
class A(Root):
    pass
```
[^164]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 48 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.360)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.360, lines 3–10)*:
```
>>>
Now, here is an implementation of the @typeassert decorator:
from inspect import signature
from functools import wraps
def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
```
[^165]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.362)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.362, lines 6–13)*:
```
the argument names to the supplied values in the same order as the function signature.
In the case of our decorator, this mapping contains the type assertions that we’re going
to enforce.
In the actual wrapper function made by the decorator, the sig.bind() method is used.
bind() is like bind_partial() except that it does not allow for missing arguments. So,
here is what happens:
>>> bound_values = sig.bind(1, 2, 3)
>>> bound_values.arguments
```
[^166]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.373)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.373, lines 6–13)*:
```
This might be a perfect use for a class decorator. For example, here is a class decorator
that rewrites the __getattribute__ special method to perform logging.
def log_getattribute(cls):
    # Get the original implementation
    orig_getattribute = cls.__getattribute__
    # Make a new definition
    def new_getattribute(self, name):
        print('getting:', name)
```
[^167]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.366)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.366, lines 39–44)*:
```
TypeError: spam() missing 1 required positional argument: 'x'
The reason it breaks is that whenever functions implementing methods are looked up
in a class, their __get__() method is invoked as part of the descriptor protocol, which
348 
| 
Chapter 9: Metaprogramming
```
[^168]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 10: Modules and Packages** *(pp.397–436)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^169]

**Annotation:** Forward reference: Chapter 10 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 11: Network and Web Programming** *(pp.437–484)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^170]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 12: Concurrency** *(pp.485–538)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^171]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 10: Modules and Packages

*Source: Python Cookbook, 3rd Edition, pages 397–436*

### Chapter Summary
This chapter covers modules and packages. Key topics include module, packages, and function. Covers file, function, class. [^172]

### Concept-by-Concept Breakdown
#### **Gil** *(p.428)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.428, lines 22–29)*:
```
sys.path.insert(0, '/other/dir')
Although this “works,” it is extremely fragile in practice and should be avoided if pos‐
sible. Part of the problem with this approach is that it adds hardcoded directory names
to your source. This can cause maintenance problems if your code ever gets moved
around to a new location. It’s usually much better to configure the path elsewhere in a
manner that can be adjusted without making source code edits.
You can sometimes work around the problem of hardcoded directories if you carefully
construct an appropriate absolute path using module-level variables, such as
```
[^173]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.433)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.433, lines 9–16)*:
```
        self._loaders = { baseurl : UrlModuleLoader(baseurl) }
    def find_module(self, fullname, path=None):
        log.debug('find_module: fullname=%r, path=%r', fullname, path)
        if path is None:
            baseurl = self._baseurl
        else:
            if not path[0].startswith(self._baseurl):
                return None
```
[^174]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Pythonpath** *(p.427)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.427, lines 29–36)*:
```
There are two common ways to get new directories added to sys.path. First, you can
add them through the use of the PYTHONPATH environment variable. For example:
    bash % env PYTHONPATH=/some/dir:/other/dir python3
    Python 3.3.0 (default, Oct  4 2012, 10:17:33)
    [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
10.9. Adding Directories to sys.path 
| 
409
```
[^175]
**Annotation:** This excerpt demonstrates 'PYTHONPATH' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.431)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.431, lines 12–19)*:
```
>>> u = urlopen('http://localhost:15000/fib.py')
>>> data = u.read().decode('utf-8')
>>> print(data)
# fib.py
print("I'm fib")
def fib(n):
    if n < 2:
        return 1
```
[^176]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.403)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.403, lines 24–31)*:
```
Discussion
Normally, to write a context manager, you define a class with an __enter__() and
__exit__() method, like this:
import time
class timethis:
    def __init__(self, label):
        self.label = label
    def __enter__(self):
```
[^177]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.403)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.403, lines 25–32)*:
```
Normally, to write a context manager, you define a class with an __enter__() and
__exit__() method, like this:
import time
class timethis:
    def __init__(self, label):
        self.label = label
    def __enter__(self):
        self.start = time.time()
```
[^178]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.416)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.416, lines 7–14)*:
```
Defining a hierarchy of modules is as easy as making a directory structure on the file‐
system. The purpose of the __init__.py files is to include optional initialization code
that runs as different levels of a package are encountered. For example, if you have the
statement import graphics, the file graphics/__init__.py will be imported and form
the contents of the graphics namespace. For an import such as import graphics.for
mats.jpg, the files graphics/__init__.py and graphics/formats/__init__.py will both be
imported prior to the final import of the graphics/formats/jpg.py file.
More often that not, it’s fine to just leave the __init__.py files empty. However, there are
```
[^179]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 11 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.426)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.426, lines 1–8)*:
```
If __main__.py is present, you can simply run the Python interpreter on the top-level
directory like this:
bash % python3 myapplication
The interpreter will execute the __main__.py file as the main program.
This technique also works if you package all of your code up into a zip file. For example:
    bash % ls
    spam.py    bar.py   grok.py   __main__.py
    bash % zip -r myapp.zip *.py
```
[^180]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.399)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.399, lines 8–15)*:
```
        self._methods = {}
        self.__name__ = func.__name__
        self._default = func
    def match(self, *types):
        def register(func):
            ndefaults = len(func.__defaults__) if func.__defaults__ else 0
            for n in range(ndefaults+1):
                self._methods[types[:len(types) - n]] = func
```
[^181]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Annotation** *(p.397)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.397, lines 10–17)*:
```
not apply this recipe directly, some of its underlying ideas might influence other pro‐
gramming techniques involving metaclasses, descriptors, and function annotations.
The main idea in the implementation is relatively simple. The MutipleMeta metaclass
uses its __prepare__() method to supply a custom class dictionary as an instance of
MultiDict. Unlike a normal dictionary, MultiDict checks to see whether entries already
exist when items are set. If so, the duplicate entries get merged together inside an in‐
stance of MultiMethod.
Instances of MultiMethod collect methods by building a mapping from type signatures
```
[^182]
**Annotation:** This excerpt demonstrates 'annotation' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.407)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.407, lines 30–37)*:
```
"Module(body=[For(target=Name(id='i', ctx=Store()),
iter=Call(func=Name(id='range', ctx=Load()), args=[Num(n=10)],
keywords=[], starargs=None, kwargs=None),
body=[Expr(value=Call(func=Name(id='print', ctx=Load()),
args=[Name(id='i', ctx=Load())], keywords=[], starargs=None,
kwargs=None))], orelse=[])])"
>>>
Analyzing the source tree requires a bit of study on your part, but it consists of a col‐
```
[^183]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.398)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.398, lines 3–10)*:
```
  File "<stdin>", line 1, in <module>
TypeError: __call__() got an unexpected keyword argument 'y'
>>> s.bar(s='hello')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: __call__() got an unexpected keyword argument 's'
>>>
There might be some way to add such support, but it would require a completely dif‐
```
[^184]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.433)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.433, lines 1–8)*:
```
except Exception as e:
        log.debug('Could not get links. %s', e)
    log.debug('links: %r', links)
    return links
class UrlMetaFinder(importlib.abc.MetaPathFinder):
    def __init__(self, baseurl):
        self._baseurl = baseurl
        self._links   = { }
```
[^185]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 27 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.401)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.401, lines 3–10)*:
```
        self._age = value
As you can see, a lot of code is being written simply to enforce some type assertions on
attribute values. Whenever you see code like this, you should explore different ways of
simplifying it. One possible approach is to make a function that simply defines the
property for you and returns it. For example:
def typed_property(name, expected_type):
    storage_name = '_' + name
    @property
```
[^186]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.401)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.401, lines 3–10)*:
```
        self._age = value
As you can see, a lot of code is being written simply to enforce some type assertions on
attribute values. Whenever you see code like this, you should explore different ways of
simplifying it. One possible approach is to make a function that simply defines the
property for you and returns it. For example:
def typed_property(name, expected_type):
    storage_name = '_' + name
    @property
```
[^187]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 11: Network and Web Programming** *(pp.437–484)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^188]

**Annotation:** Forward reference: Chapter 11 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 12: Concurrency** *(pp.485–538)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, __enter__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^189]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 13: Utility Scripting and System Administration** *(pp.539–564)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^190]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 11: Network and Web Programming

*Source: Python Cookbook, 3rd Edition, pages 437–484*

### Chapter Summary
This chapter covers network and web programming. Key topics include module, package, and function. Covers file, function. [^191]

### Concept-by-Concept Breakdown
#### **None** *(p.440)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.440, lines 19–26)*:
```
...             print('Looking for', fullname, path)
...             return None
...
>>> import sys
>>> sys.meta_path.insert(0, Finder())   # Insert as first entry
>>> import math
Looking for math None
>>> import types
```
[^192]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 11 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.468)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.468, lines 4–11)*:
```
    resp = _hello_resp.format(name=params.get('name'))
    yield resp.encode('utf-8')
_localtime_resp = '''\
<?xml version="1.0"?>
<time>
  <year>{t.tm_year}</year>
  <month>{t.tm_mon}</month>
  <day>{t.tm_mday}</day>
```
[^193]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.444)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.444, lines 16–23)*:
```
For a normal package, find_loader() returns a tuple (loader, path) where loader
is the loader instance that will import the package (and execute __init__.py) and path
is a list of the directories that will make up the initial setting of the package’s __path__
attribute. For example, if the base URL was http://localhost:15000 and a user exe‐
cuted import grok, the path returned by find_loader() would be [ 'http://local
host:15000/grok' ].
The find_loader() must additionally account for the possibility of a namespace pack‐
age. A namespace package is a package where a valid package directory name exists,
```
[^194]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.461)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.461, lines 1–8)*:
```
if __name__ == '__main__':
    serv = ThreadingTCPServer(('', 20000), EchoHandler)
    serv.serve_forever()
One issue with forking and threaded servers is that they spawn a new process or thread
on each client connection. There is no upper bound on the number of allowed clients,
so a malicious hacker could potentially launch a large number of simultaneous con‐
nections in an effort to make your server explode.
If this is a concern, you can create a pre-allocated pool of worker threads or processes.
```
[^195]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.461)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.461, lines 1–8)*:
```
if __name__ == '__main__':
    serv = ThreadingTCPServer(('', 20000), EchoHandler)
    serv.serve_forever()
One issue with forking and threaded servers is that they spawn a new process or thread
on each client connection. There is no upper bound on the number of allowed clients,
so a malicious hacker could potentially launch a large number of simultaneous con‐
nections in an effort to make your server explode.
If this is a concern, you can create a pre-allocated pool of worker threads or processes.
```
[^196]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.479)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.479, lines 6–13)*:
```
                # Receive a message
                func_name, args, kwargs = json.loads(connection.recv())
                # Run the RPC and send a response
                try:
                    r = self._functions[func_name](*args,**kwargs)
                    connection.send(json.dumps(r))
                except Exception as e:
                    connection.send(json.dumps(str(e)))
```
[^197]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.470)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.470, lines 4–11)*:
```
from the request and puts them into a dictionary-like object for later use.
The start_response argument is a function that must be called to initiate a response.
The first argument is the resulting HTTP status. The second argument is a list of (name,
value) tuples that make up the HTTP headers of the response. For example:
def wsgi_app(environ, start_response):
    ...
    start_response('200 OK', [('Content-type', 'text/plain')])
To return data, an WSGI application must return a sequence of byte strings. This can
```
[^198]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.465)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.465, lines 38–45)*:
```
>>>
Network objects also allow indexing like arrays. For example:
>>> net.num_addresses
32
>>> net[0]
11.4. Generating a Range of IP Addresses from a CIDR Address 
| 
447
```
[^199]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.441)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.441, lines 15–22)*:
```
Now you don’t see any output because the imports are being handled by other entries
in sys.meta_path. In this case, you would only see it trigger when nonexistent modules
are imported:
>>> import fib
Looking for fib None
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named 'fib'
```
[^200]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 18 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.444)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.444, lines 18–25)*:
```
is a list of the directories that will make up the initial setting of the package’s __path__
attribute. For example, if the base URL was http://localhost:15000 and a user exe‐
cuted import grok, the path returned by find_loader() would be [ 'http://local
host:15000/grok' ].
The find_loader() must additionally account for the possibility of a namespace pack‐
age. A namespace package is a package where a valid package directory name exists,
but no __init__.py file can be found. For this case, find_loader() must return a tuple
(None, path) where path is a list of directories that would have made up the package’s
```
[^201]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.460)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.460, lines 2–9)*:
```
            if not msg:
                break
            self.request.send(msg)
if __name__ == '__main__':
    serv = TCPServer(('', 20000), EchoHandler)
    serv.serve_forever()
In this code, you define a special handler class that implements a handle() method for
servicing client connections. The request attribute is the underlying client socket and
```
[^202]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.440)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.440, lines 8–15)*:
```
>>> pprint(sys.meta_path)
[<class '_frozen_importlib.BuiltinImporter'>,
 <class '_frozen_importlib.FrozenImporter'>,
 <class '_frozen_importlib.PathFinder'>]
>>>
When executing a statement such as import fib, the interpreter walks through the
finder objects on sys.meta_path and invokes their find_module() method in order to
locate an appropriate module loader. It helps to see this by experimentation, so define
```
[^203]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.482)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.482, lines 19–26)*:
```
        s.send(data)
    s.close()
    print('Connection closed')
def echo_server(address):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(1)
    # Wrap with an SSL layer requiring client certs
```
[^204]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Closure** *(p.478)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.478, lines 17–24)*:
```
('foo', (1, 2), {'z': 3}) that contains the function name and arguments. This
tuple is pickled and sent over the connection. This is performed in the do_rpc() closure
that’s returned by the __getattr__() method of RPCProxy. The server receives and
unpickles the message, looks up the function name to see if it’s registered, and executes
it with the given arguments. The result (or exception) is then pickled and sent back.
As shown, the example relies on multiprocessing for communication. However, this
approach could be made to work with just about any other messaging system. For ex‐
ample, if you want to implement RPC over ZeroMQ, just replace the connection objects
```
[^205]
**Annotation:** This excerpt demonstrates 'closure' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Collections** *(p.442)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.442, lines 16–23)*:
```
 '/usr/local/lib/python3.3/': FileFinder('/usr/local/lib/python3.3/'),
 '/usr/local/lib/python3.3/collections': FileFinder('...python3.3/collections'),
 '/usr/local/lib/python3.3/encodings': FileFinder('...python3.3/encodings'),
 '/usr/local/lib/python3.3/lib-dynload': FileFinder('...python3.3/lib-dynload'),
 '/usr/local/lib/python3.3/plat-darwin': FileFinder('...python3.3/plat-darwin'),
 '/usr/local/lib/python3.3/site-packages': FileFinder('...python3.3/site-packages'),
 '/usr/local/lib/python33.zip': None}
>>>
```
[^206]
**Annotation:** This excerpt demonstrates 'collections' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 12: Concurrency** *(pp.485–538)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^207]

**Annotation:** Forward reference: Chapter 12 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 13: Utility Scripting and System Administration** *(pp.539–564)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^208]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 14: Testing, Debugging, and Exceptions** *(pp.565–596)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^209]

**Annotation:** Forward reference: Chapter 14 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 12: Concurrency

*Source: Python Cookbook, 3rd Edition, pages 485–538*

### Chapter Summary
Adding SSL to Network Services 
| 
467 As shown, the server presents a certificate to the client and the client verifies it Key topics include threading, functions, and object. Covers file, function. [^210]

### Concept-by-Concept Breakdown
#### **Gil** *(p.533)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.533, lines 14–21)*:
```
    pool = multiprocessing.Pool()
This example with a pool works around the GIL using a neat trick. Whenever a thread
wants to perform CPU-intensive work, it hands the work to the pool. The pool, in turn,
hands the work to a separate Python interpreter running in a different process. While
the thread is waiting for the result, it releases the GIL. Moreover, because the calculation
is being performed in a separate interpreter, it’s no longer bound by the restrictions of
the GIL. On a multicore system, you’ll find that this technique easily allows you to take
advantage of all the CPUs.
```
[^211]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.485)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.485, lines 3–10)*:
```
>>> from xmlrpc.client import ServerProxy
>>> s = ServerProxy('https://localhost:15000', allow_none=True)
>>> s.set('foo','bar')
>>> s.set('spam', [1, 2, 3])
>>> s.keys()
['spam', 'foo']
>>> s.get('foo')
'bar'
```
[^212]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.520)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.520, lines 25–32)*:
```
    with acquire(y_lock):
  File "/usr/local/lib/python3.3/contextlib.py", line 48, in __enter__
    return next(self.gen)
  File "deadlock.py", line 15, in acquire
    raise RuntimeError("Lock Order Violation")
RuntimeError: Lock Order Violation
>>>
This crash is caused by the fact that each thread remembers the locks it has already
```
[^213]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.522)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.522, lines 26–33)*:
```
        return self.local.sock
    def __exit__(self, exc_ty, exc_val, tb):
        self.local.sock.close()
        del self.local.sock
In this code, carefully observe the use of the self.local attribute. It is initialized as an
instance of threading.local(). The other methods then manipulate a socket that’s
stored as self.local.sock. This is enough to make it possible to safely use an instance
of LazyConnection in multiple threads. For example:
```
[^214]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.485)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.485, lines 24–31)*:
```
class VerifyCertSafeTransport(SafeTransport):
    def __init__(self, cafile, certfile=None, keyfile=None):
        SafeTransport.__init__(self)
        self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self._ssl_context.load_verify_locations(cafile)
        if cert:
            self._ssl_context.load_cert_chain(certfile, keyfile)
        self._ssl_context.verify_mode = ssl.CERT_REQUIRED
```
[^215]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.491)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.491, lines 2–9)*:
```
        client.close()
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: server.py server_address port', file=sys.stderr)
        raise SystemExit(1)
    server(sys.argv[1], int(sys.argv[2]))
To run this server, you would run a command such as python3 servermp.py /tmp/
```
[^216]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.491)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.491, lines 2–9)*:
```
        client.close()
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: server.py server_address port', file=sys.stderr)
        raise SystemExit(1)
    server(sys.argv[1], int(sys.argv[2]))
To run this server, you would run a command such as python3 servermp.py /tmp/
```
[^217]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.538)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.538, lines 5–12)*:
```
class Worker(Actor):
    def submit(self, func, *args, **kwargs):
        r = Result()
        self.send((func, args, kwargs, r))
        return r
    def run(self):
        while True:
            func, args, kwargs, r = self.recv()
```
[^218]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 8 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.485)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.485, lines 33–40)*:
```
        # Items in the passed dictionary are passed as keyword
        # arguments to the http.client.HTTPSConnection() constructor.
        # The context argument allows an ssl.SSLContext instance to
        # be passed with information about the SSL configuration
        s = super().make_connection((host, {'context': self._ssl_context}))
        return s
# Create the client proxy
s = ServerProxy('https://localhost:15000',
```
[^219]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Array** *(p.501)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.501, lines 1–8)*:
```
This recipe gets around this by playing a sneaky trick with memoryviews. Essentially, a
memoryview is an overlay of an existing array. Not only that, memoryviews can be cast
to different types to allow interpretation of the data in a different manner. This is the
purpose of the following statement:
view = memoryview(arr).cast('B')
It takes an array arr and casts into a memoryview of unsigned bytes.
In this form, the view can be passed to socket-related functions, such as sock.send()
or send.recv_into(). Under the covers, those methods are able to work directly with
```
[^220]
**Annotation:** This excerpt demonstrates 'array' as it appears in the primary text. The concept occurs 7 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.516)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.516, lines 1–8)*:
```
In older Python code, it is common to see locks explicitly acquired and released. For
example, in this variant of the last example:
import threading
class SharedCounter:
    '''
    A counter object that can be shared by multiple threads.
    '''
    def __init__(self, initial_value = 0):
```
[^221]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 16 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.492)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.492, lines 8–15)*:
```
    ack = sock.recv(2)
    assert ack == b'OK'
def server(work_address, port):
    # Wait for the worker to connect
    work_serv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    work_serv.bind(work_address)
    work_serv.listen(1)
    worker, addr = work_serv.accept()
```
[^222]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.493)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.493, lines 27–34)*:
```
Problem
You have heard about packages based on “event-driven” or “asynchronous” I/O, but
you’re not entirely sure what it means, how it actually works under the covers, or how
it might impact your program if you use it.
Solution
At a fundamental level, event-driven I/O is a technique that takes basic I/O operations
(e.g., reads and writes) and converts them into events that must be handled by your
program. For example, whenever data was received on a socket, it turns into a “receive”
```
[^223]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.522)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.522, lines 7–14)*:
```
the currently executing thread. To do this, create a thread-local storage object using
threading.local(). Attributes stored and read on this object are only visible to the
executing thread and no others.
As an interesting practical example of using thread-local storage, consider the LazyCon
nection context-manager class that was first defined in Recipe 8.3. Here is a slightly
modified version that safely works with multiple threads:
from socket import socket, AF_INET, SOCK_STREAM
import threading
```
[^224]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.524)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.524, lines 14–21)*:
```
        if not msg:
            break
        sock.sendall(msg)
    print('Client closed connection')
    sock.close()
def echo_server(addr):
    pool = ThreadPoolExecutor(128)
    sock = socket(AF_INET, SOCK_STREAM)
```
[^225]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 13: Utility Scripting and System Administration** *(pp.539–564)*

This later chapter builds upon the concepts introduced here, particularly: None, __init__, __main__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^226]

**Annotation:** Forward reference: Chapter 13 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __init__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 14: Testing, Debugging, and Exceptions** *(pp.565–596)*

This later chapter builds upon the concepts introduced here, particularly: None, __enter__, __exit__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^227]

**Annotation:** Forward reference: Chapter 14 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, __enter__ appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 15: C Extensions** *(pp.597–706)*

This later chapter builds upon the concepts introduced here, particularly: GIL, None, __enter__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^228]

**Annotation:** Forward reference: Chapter 15 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts GIL, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 13: Utility Scripting and System Administration

*Source: Python Cookbook, 3rd Edition, pages 539–564*

### Chapter Summary
Here is a simple example that shows how to use an exchange:
# Example of a task Key topics include generators, function, and concurrency. Covers file, generator, function. [^229]

### Concept-by-Concept Breakdown
#### **None** *(p.546)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.546, lines 1–8)*:
```
self._ready.append((task, None))
        self._numtasks += 1
    def add_ready(self, task, msg=None):
        '''
        Append an already started task to the ready queue.
        msg is what to send into the task when it resumes.
        '''
        self._ready.append((task, msg))
```
[^230]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.564)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.564, lines 6–13)*:
```
interpret the resulting bytes as text, add a further decoding step. For example:
out_text = out_bytes.decode('utf-8')
If the executed command returns a nonzero exit code, an exception is raised. Here is
an example of catching errors and getting the output created along with the exit code:
try:
    out_bytes = subprocess.check_output(['cmd','arg1','arg2'])
except subprocess.CalledProcessError as e:
    out_bytes = e.output       # Output generated before error
```
[^231]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.547)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.547, lines 5–12)*:
```
class AcceptSocket(YieldEvent):
    def __init__(self, sock):
        self.sock = sock
    def handle_yield(self, sched, task):
        sched._read_wait(self.sock.fileno(), self, task)
    def handle_resume(self, sched, task):
        r = self.sock.accept()
        sched.add_ready(task, r)
```
[^232]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.544)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.544, lines 31–38)*:
```
# Example use
if __name__ == '__main__':
    def printer():
        while True:
            msg = yield
            print('Got:', msg)
    def counter(sched):
        while True:
```
[^233]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.544)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.544, lines 31–38)*:
```
# Example use
if __name__ == '__main__':
    def printer():
        while True:
            msg = yield
            print('Got:', msg)
    def counter(sched):
        while True:
```
[^234]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argparse** *(p.559)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.559, lines 13–20)*:
```
Solution
The argparse module can be used to parse command-line options. A simple example
will help to illustrate the essential features:
# search.py
'''
Hypothetical command-line tool for searching a collection of
files for one or more text patterns.
'''
```
[^235]
**Annotation:** This excerpt demonstrates 'argparse' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.560)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.560, lines 1–8)*:
```
# Output the collected arguments
print(args.filenames)
print(args.patterns)
print(args.verbose)
print(args.outfile)
print(args.speed)
This program defines a command-line parser with the following usage:
bash % python3 search.py -h
```
[^236]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.561)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.561, lines 6–13)*:
```
be used and extended to get started.
To parse options, you first create an ArgumentParser instance and add declarations for
the options you want to support it using the add_argument() method. In each add_ar
gument() call, the dest argument specifies the name of an attribute where the result of
parsing will be placed. The metavar argument is used when generating help messages.
The action argument specifies the processing associated with the argument and is often
store for storing a value or append for collecting multiple argument values into a list.
The following argument collects all of the extra command-line arguments into a list. It’s
```
[^237]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 22 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.546)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.546, lines 1–8)*:
```
self._ready.append((task, None))
        self._numtasks += 1
    def add_ready(self, task, msg=None):
        '''
        Append an already started task to the ready queue.
        msg is what to send into the task when it resumes.
        '''
        self._ready.append((task, msg))
```
[^238]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 27 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Async** *(p.549)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.549, lines 26–33)*:
```
342 and “A Curious Course on Coroutines and Concurrency”.
PEP 3156 also has a modern take on asynchronous I/O involving coroutines. In practice,
it is extremelyunlikely that you will write a low-level coroutine scheduler yourself.
However, ideas surrounding coroutines are the basis for many popular libraries, in‐
cluding gevent, greenlet, Stackless Python, and similar projects.
12.13. Polling Multiple Thread Queues
Problem
You have a collection of thread queues, and you would like to be able to poll them for
```
[^239]
**Annotation:** This excerpt demonstrates 'async' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.561)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.561, lines 8–15)*:
```
the options you want to support it using the add_argument() method. In each add_ar
gument() call, the dest argument specifies the name of an attribute where the result of
parsing will be placed. The metavar argument is used when generating help messages.
The action argument specifies the processing associated with the argument and is often
store for storing a value or append for collecting multiple argument values into a list.
The following argument collects all of the extra command-line arguments into a list. It’s
being used to make a list of filenames in the example:
parser.add_argument(dest='filenames',metavar='filename', nargs='*')
```
[^240]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.561)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.561, lines 15–22)*:
```
parser.add_argument(dest='filenames',metavar='filename', nargs='*')
The following argument sets a Boolean flag depending on whether or not the argument
was provided:
parser.add_argument('-v', dest='verbose', action='store_true',
                    help='verbose mode')
The following argument takes a single value and stores it as a string:
parser.add_argument('-o', dest='outfile', action='store',
                    help='output file')
```
[^241]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Break** *(p.547)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.547, lines 34–41)*:
```
            if not c:
                break
            chars.append(c)
            if c == b'\n':
                break
        return b''.join(chars)
    # Echo server using generators
    class EchoServer:
```
[^242]
**Annotation:** This excerpt demonstrates 'break' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Class** *(p.545)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.545, lines 16–23)*:
```
from select import select
# This class represents a generic yield event in the scheduler
class YieldEvent:
    def handle_yield(self, sched, task):
        pass
    def handle_resume(self, sched, task):
        pass
# Task Scheduler
```
[^243]
**Annotation:** This excerpt demonstrates 'class' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Close** *(p.548)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.548, lines 15–22)*:
```
                    line = line[nsent:]
            client.close()
            print('Client closed')
    sched = Scheduler()
    EchoServer(('',16000),sched)
    sched.run()
This code will undoubtedly require a certain amount of careful study. However, it is
essentially implementing a small operating system. There is a queue of tasks ready to
```
[^244]
**Annotation:** This excerpt demonstrates 'close' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 14: Testing, Debugging, and Exceptions** *(pp.565–596)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^245]

**Annotation:** Forward reference: Chapter 14 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.


**Chapter 15: C Extensions** *(pp.597–706)*

This later chapter builds upon the concepts introduced here, particularly: None, UTF-8, __init__.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^246]

**Annotation:** Forward reference: Chapter 15 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts None, UTF-8 appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 14: Testing, Debugging, and Exceptions

*Source: Python Cookbook, 3rd Edition, pages 565–596*

### Chapter Summary
This chapter covers testing, debugging, and exceptions. Key topics include exceptions, functions, and module. Covers file, function, class. [^247]

### Concept-by-Concept Breakdown
#### **Mro** *(p.594)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.594, lines 24–31)*:
```
As a debugging tip, if you’re not entirely sure about the class hierarchy of a particular
exception, you can quickly view it by inspecting the exception’s __mro__ attribute. For
example:
>>> FileNotFoundError.__mro__
(<class 'FileNotFoundError'>, <class 'OSError'>, <class 'Exception'>,
 <class 'BaseException'>, <class 'object'>)
>>>
Any one of the listed classes up to BaseException can be used with the except statement.
```
[^248]
**Annotation:** This excerpt demonstrates 'MRO' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.578)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.578, lines 5–12)*:
```
        self._func = func
        self._start = None
    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()
    def stop(self):
        if self._start is None:
```
[^249]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 5 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.565)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.565, lines 16–23)*:
```
# To interpret as text, decode
out = stdout.decode('utf-8')
err = stderr.decode('utf-8')
The subprocess module is not suitable for communicating with external commands
that expect to interact with a proper TTY. For example, you can’t use it to automate tasks
that ask the user to enter a password (e.g., a ssh session). For that, you would need to
turn to a third-party module, such as those based on the popular “expect” family of tools
(e.g., pexpect or similar).
```
[^250]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.578)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.578, lines 21–28)*:
```
        return self._start is not None
    def __enter__(self):
        self.start()
        return self
    def __exit__(self, *args):
        self.stop()
This class defines a timer that can be started, stopped, and reset as needed by the user.
It keeps track of the total elapsed time in the elapsed attribute. Here is an example that
```
[^251]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.578)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.578, lines 24–31)*:
```
        return self
    def __exit__(self, *args):
        self.stop()
This class defines a timer that can be started, stopped, and reset as needed by the user.
It keeps track of the total elapsed time in the elapsed attribute. Here is an example that
shows how it can be used:
def countdown(n):
    while n > 0:
```
[^252]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.578)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.578, lines 2–9)*:
```
class Timer:
    def __init__(self, func=time.perf_counter):
        self.elapsed = 0.0
        self._func = func
        self._start = None
    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
```
[^253]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.592)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.592, lines 6–13)*:
```
        self.assertEqual(2+2, 5)
if __name__ == '__main__':
    unittest.main()
If you run this code on a Mac, you’ll get this output:
    bash % python3 testsample.py -v
    test_0 (__main__.Tests) ... ok
    test_1 (__main__.Tests) ... skipped 'skipped test'
    test_2 (__main__.Tests) ... skipped 'Not supported on Unix'
```
[^254]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.590)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.590, lines 12–19)*:
```
    ...
if __name__ == '__main__':
    unittest.main()
This makes the test file executable, and prints the results of running tests to standard
output. If you would like to redirect this output, you need to unwind the main() call a
bit and write your own main() function like this:
import sys
def main(out=sys.stderr, verbosity=2):
```
[^255]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.567)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.567, lines 21–28)*:
```
except shutil.Error as e:
    for src, dst, msg in e.args[0]:
         # src is source name
         # dst is destination name
         # msg is error message from exception
         print(dst, src, msg)
If you supply the ignore_dangling_symlinks=True keyword argument, then copy
tree() will ignore dangling symlinks.
```
[^256]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.574)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.574, lines 9–16)*:
```
The five logging calls (critical(), error(), warning(), info(), debug()) represent
different severity levels in decreasing order. The level argument to basicConfig() is
a filter. All messages issued at a level lower than this setting will be ignored.
The argument to each logging operation is a message string followed by zero or more
arguments. When making the final log message, the % operator is used to format the
message string using the supplied arguments.
If you run this program, the contents of the file app.log will be as follows:
    CRITICAL:root:Host www.python.org unknown
```
[^257]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **As** *(p.589)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.589, lines 3–10)*:
```
Discussion
The assertRaises() method provides a convenient way to test for the presence of an
exception. A common pitfall is to write tests that manually try to do things with excep‐
tions on their own. For instance:
class TestConversion(unittest.TestCase):
    def test_bad_int(self):
        try:
            r = parse_int('N/A')
```
[^258]
**Annotation:** This excerpt demonstrates 'as' as it appears in the primary text. The concept occurs 26 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assert** *(p.589)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.589, lines 3–10)*:
```
Discussion
The assertRaises() method provides a convenient way to test for the presence of an
exception. A common pitfall is to write tests that manually try to do things with excep‐
tions on their own. For instance:
class TestConversion(unittest.TestCase):
    def test_bad_int(self):
        try:
            r = parse_int('N/A')
```
[^259]
**Annotation:** This excerpt demonstrates 'assert' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Assertion** *(p.586)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.586, lines 26–33)*:
```
mimic callables and instances. They record information about usage and allow you to
make assertions. For example:
>>> from unittest.mock import MagicMock
>>> m = MagicMock(return_value = 10)
>>> m(1, 2, debug=True)
10
>>> m.assert_called_with(1, 2, debug=True)
>>> m.assert_called_with(1, 2)
```
[^260]
**Annotation:** This excerpt demonstrates 'assertion' as it appears in the primary text. The concept occurs 3 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Attribute** *(p.578)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.578, lines 27–34)*:
```
This class defines a timer that can be started, stopped, and reset as needed by the user.
It keeps track of the total elapsed time in the elapsed attribute. Here is an example that
shows how it can be used:
def countdown(n):
    while n > 0:
        n -= 1
# Use 1: Explicit start/stop
t = Timer()
```
[^261]
**Annotation:** This excerpt demonstrates 'attribute' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Boolean** *(p.570)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.570, lines 39–43)*:
```
'/usr/local/lib'
>>> cfg.getboolean('debug','log_errors')
552 
| 
Chapter 13: Utility Scripting and System Administration
```
[^262]
**Annotation:** This excerpt demonstrates 'boolean' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


#### **Later Chapters in This Book**


**Chapter 15: C Extensions** *(pp.597–706)*

This later chapter builds upon the concepts introduced here, particularly: MRO, None, UTF-8.... The material extends the foundational understanding established in this chapter by exploring more advanced applications, deeper implementation details, or integration with other Python features. Readers seeking to deepen their mastery of these topics should plan to revisit this chapter after completing the current material.
[^263]

**Annotation:** Forward reference: Chapter 15 shares 5 concept(s) with this chapter, indicating topical continuity and progressive skill development. The concepts MRO, None appear in both contexts, suggesting that understanding from this chapter will directly transfer to and be expanded upon in the later material.



---

## Chapter 15: C Extensions

*Source: Python Cookbook, 3rd Edition, pages 597–706*

### Chapter Summary
This chapter covers c extensions. Key topics include function, module, and object. Covers function, file. [^264]

### Concept-by-Concept Breakdown
#### **Gil** *(p.642)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.642, lines 1–8)*:
```
A final tricky part of calling into Python from C concerns the management of Python’s
global interpreter lock (GIL). Whenever Python is accessed from C, you need to make
sure that the GIL is properly acquired and released. Otherwise, you run the risk of having
the interpreter corrupt data or crash. The calls to PyGILState_Ensure() and PyGIL
State_Release() make sure that it’s done correctly:
double call_func(PyObject *func, double x, double y) {
  ...
  double retval;
```
[^265]
**Annotation:** This excerpt demonstrates 'GIL' as it appears in the primary text. The concept occurs 15 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Mro** *(p.696)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.696, lines 33–40)*:
```
moving directories/files, 547
__mro__ attribute, 576
multidicts, 11–12
multiple-dispatch, 376–382
multiprocessing module, 488
GIL and, 514
passing file descriptors with, 470–475
reduction module, 470–475
```
[^266]
**Annotation:** This excerpt demonstrates 'MRO' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **None** *(p.599)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.599, lines 26–33)*:
```
exception.
If, for some reason, you want to suppress chaining, use raise from None:
>>> def example3():
...     try:
...             int('N/A')
...     except ValueError:
...             raise RuntimeError('A parsing error occurred') from None...
>>> 
```
[^267]
**Annotation:** This excerpt demonstrates 'None' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Pythonpath** *(p.699)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.699, lines 34–41)*:
```
Python syntax vs. JSON, 180
PYTHONPATH environment variable, 409
pytz module, 110–112
PyUnicode_FromWideChar() function (C ex‐
tensions)
C strings, converting to Python objects, 653–
654
pyvenv command, 432–433
```
[^268]
**Annotation:** This excerpt demonstrates 'PYTHONPATH' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Utf-8** *(p.674)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.674, lines 6–13)*:
```
>>> raw = b'Spicy Jalape\xc3\xb1o\xae'
>>> raw.decode('utf-8','ignore')
'Spicy Jalapeño'
>>> raw.decode('utf-8','replace')
'Spicy Jalapeño?'
>>>
The surrogateescape error handling policies takes all nondecodable bytes and turns
them into the low-half of a surrogate pair (\udcXX where XX is the raw byte value). For
```
[^269]
**Annotation:** This excerpt demonstrates 'UTF-8' as it appears in the primary text. The concept occurs 6 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Enter__** *(p.690)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.690, lines 55–62)*:
```
pattern matching with, 42
__enter__() method (with statements), 246–248
enumerate() function, 127–128
environ argument (WSGI), 451
error messages, terminating program with, 540
error() function (logging module), 556
escape() function (html module), 65
escape() function (xml.sax.saxutils module), 191
```
[^270]
**Annotation:** This excerpt demonstrates '__enter__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Exit__** *(p.690)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.690, lines 80–87)*:
```
execve() function (os module), 546
__exit__() method (with statements), 246–248
@expectedFailure decorator, 574
exponential notation, 87
%extend directive (Swig), 630
external command
executing, 545
getting output, 545
```
[^271]
**Annotation:** This excerpt demonstrates '__exit__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Init__** *(p.597)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.597, lines 18–25)*:
```
    ...
If you are going to define a new exception that overrides the __init__() method of
Exception, make sure you always call Exception.__init__() with all of the passed
arguments. For example:
class CustomError(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = message
```
[^272]
**Annotation:** This excerpt demonstrates '__init__' as it appears in the primary text. The concept occurs 4 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Main__** *(p.611)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.611, lines 21–28)*:
```
>>> a = A(1,2)
>>> timeit('a.x', 'from __main__ import a')
0.07817923510447145
>>> timeit('a.y', 'from __main__ import a')
0.35766440676525235
>>>
As you can observe, accessing the property y is not just slightly slower than a simple
attribute x, it’s about 4.5 times slower. If this difference matters, you should ask yourself
```
[^273]
**Annotation:** This excerpt demonstrates '__main__' as it appears in the primary text. The concept occurs 2 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **__Name__** *(p.606)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.606, lines 29–36)*:
```
        end = time.perf_counter()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper
To use this decorator, you simply place it in front of a function definition to get timings
from it. For example:
>>> @timethis
... def countdown(n):
```
[^274]
**Annotation:** This excerpt demonstrates '__name__' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Abstraction** *(p.611)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.611, lines 5–12)*:
```
             op(value)
Avoid gratuitous abstraction
Any time you wrap up code with extra layers of processing, such as decorators, prop‐
erties, or descriptors, you’re going to make it slower. As an example, consider this class:
class A:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```
[^275]
**Annotation:** This excerpt demonstrates 'abstraction' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Annotation** *(p.686)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.686, lines 19–26)*:
```
arguments
annotations, 220
cleaning up in C extensions, 623
multiple-dispatch, implementing with, 376–
382
arrays
calculating with large numerical, 97–100
high-performance with Cython, 638–642
```
[^276]
**Annotation:** This excerpt demonstrates 'annotation' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argparse** *(p.686)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.686, lines 15–22)*:
```
unpacking, 549
argparse module, 541, 543, 544
.args attribute (Exceptions), 579
ArgumentParser instance, 543
arguments
annotations, 220
cleaning up in C extensions, 623
multiple-dispatch, implementing with, 376–
```
[^277]
**Annotation:** This excerpt demonstrates 'argparse' as it appears in the primary text. The concept occurs 1 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Args** *(p.624)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.624, lines 6–13)*:
```
/* int gcd(int, int) */
static PyObject *py_gcd(PyObject *self, PyObject *args) {
  int x, y, result;
  if (!PyArg_ParseTuple(args,"ii", &x, &y)) {
    return NULL;
  }
  result = gcd(x,y);
  return Py_BuildValue("i", result);
```
[^278]
**Annotation:** This excerpt demonstrates 'args' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.


#### **Argument** *(p.649)*

**Verbatim Educational Excerpt** *(Python Cookbook 3rd, p.649, lines 5–12)*:
```
The second customization involving the inclusion of the typemaps.i library and the 
%apply directive is instructing Swig that the argument signature int *remainder is to
be treated as an output value. This is actually a pattern matching rule. In all declarations
that follow, any time int *remainder is encountered, it is handled as output. This
customization is what makes the divide() function return two values:
>>> sample.divide(42,8)
[5, 2]
>>>
```
[^279]
**Annotation:** This excerpt demonstrates 'argument' as it appears in the primary text. The concept occurs 9 time(s) on this page, making it a key anchor point for understanding how the text introduces and develops this topic. Use this passage to verify precise terminology, definitions, and contextual usage patterns.



### **TPM Implementation Section** *(ORIGINAL)*

_Not enough source material found to derive implementation._


### **See Also: Cross-Book References & Forward Connections**


---


---

### **Footnotes**

[^1]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 1, lines 1–25).
[^2]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 10, lines 32–39).
[^3]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 35, lines 22–29).
[^4]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 27, lines 4–11).
[^5]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 24, lines 8–15).
[^6]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 24, lines 8–15).
[^7]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 27, lines 16–23).
[^8]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 9, lines 26–33).
[^9]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 22, lines 22–29).
[^10]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 8, lines 7–14).
[^11]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 6, lines 25–32).
[^12]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 9, lines 1–8).
[^13]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 8, lines 26–33).
[^14]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 9, lines 4–11).
[^15]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 26, lines 26–33).
[^16]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 8, lines 19–26).
[^17]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 37, lines 1–1).
[^18]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 83, lines 1–1).
[^19]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 113, lines 1–1).
[^20]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 37, lines 1–25).
[^21]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 50, lines 3–10).
[^22]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 41, lines 33–38).
[^23]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 42, lines 1–8).
[^24]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 51, lines 5–12).
[^25]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 41, lines 1–8).
[^26]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 49, lines 19–26).
[^27]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 46, lines 3–10).
[^28]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 48, lines 29–36).
[^29]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 80, lines 8–15).
[^30]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 66, lines 1–8).
[^31]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 48, lines 1–8).
[^32]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 63, lines 13–20).
[^33]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 47, lines 1–8).
[^34]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 59, lines 1–8).
[^35]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 81, lines 34–41).
[^36]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 83, lines 1–1).
[^37]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 113, lines 1–1).
[^38]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 141, lines 1–1).
[^39]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 83, lines 1–25).
[^40]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 89, lines 15–22).
[^41]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 98, lines 34–41).
[^42]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 83, lines 30–37).
[^43]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 97, lines 10–17).
[^44]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 83, lines 8–15).
[^45]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 98, lines 23–30).
[^46]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 91, lines 24–31).
[^47]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 88, lines 4–11).
[^48]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 86, lines 2–9).
[^49]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 95, lines 2–9).
[^50]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 90, lines 13–20).
[^51]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 89, lines 42–47).
[^52]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 98, lines 26–33).
[^53]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 91, lines 6–13).
[^54]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 98, lines 30–37).
[^55]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 113, lines 1–1).
[^56]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 141, lines 1–1).
[^57]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 175, lines 1–1).
[^58]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 113, lines 1–25).
[^59]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 137, lines 5–12).
[^60]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 133, lines 1–8).
[^61]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 133, lines 11–18).
[^62]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 133, lines 11–18).
[^63]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 133, lines 4–11).
[^64]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 123, lines 23–30).
[^65]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 115, lines 1–8).
[^66]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 139, lines 1–8).
[^67]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 139, lines 16–23).
[^68]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 132, lines 4–11).
[^69]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 139, lines 2–9).
[^70]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 139, lines 4–11).
[^71]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 124, lines 5–12).
[^72]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 138, lines 15–22).
[^73]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 130, lines 17–24).
[^74]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 141, lines 1–1).
[^75]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 175, lines 1–1).
[^76]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 217, lines 1–1).
[^77]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 141, lines 1–25).
[^78]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 142, lines 14–21).
[^79]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 160, lines 9–16).
[^80]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 162, lines 1–8).
[^81]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 165, lines 8–15).
[^82]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 152, lines 19–26).
[^83]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 162, lines 13–20).
[^84]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 142, lines 33–40).
[^85]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 167, lines 1–8).
[^86]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 160, lines 27–34).
[^87]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 153, lines 18–25).
[^88]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 172, lines 31–38).
[^89]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 154, lines 28–35).
[^90]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 174, lines 10–17).
[^91]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 151, lines 2–9).
[^92]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 167, lines 32–39).
[^93]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 175, lines 1–1).
[^94]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 217, lines 1–1).
[^95]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 243, lines 1–1).
[^96]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 175, lines 1–25).
[^97]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 198, lines 4–11).
[^98]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 182, lines 2–9).
[^99]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 200, lines 6–13).
[^100]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 200, lines 22–29).
[^101]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 200, lines 27–34).
[^102]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 212, lines 16–23).
[^103]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 186, lines 18–25).
[^104]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 191, lines 37–44).
[^105]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 215, lines 1–8).
[^106]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 203, lines 26–33).
[^107]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 181, lines 15–22).
[^108]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 179, lines 1–8).
[^109]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 200, lines 5–12).
[^110]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 184, lines 17–24).
[^111]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 194, lines 6–13).
[^112]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 217, lines 1–1).
[^113]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 243, lines 1–1).
[^114]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 329, lines 1–1).
[^115]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 217, lines 1–25).
[^116]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 240, lines 14–21).
[^117]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 224, lines 5–12).
[^118]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 229, lines 7–14).
[^119]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 218, lines 13–20).
[^120]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 238, lines 11–18).
[^121]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 236, lines 19–26).
[^122]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 236, lines 1–8).
[^123]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 217, lines 19–26).
[^124]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 217, lines 1–8).
[^125]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 219, lines 19–26).
[^126]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 220, lines 29–36).
[^127]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 225, lines 8–15).
[^128]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 228, lines 36–43).
[^129]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 228, lines 14–21).
[^130]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 235, lines 5–12).
[^131]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 243, lines 1–1).
[^132]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 329, lines 1–1).
[^133]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 397, lines 1–1).
[^134]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 243, lines 1–25).
[^135]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 268, lines 21–28).
[^136]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 276, lines 30–37).
[^137]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 284, lines 10–17).
[^138]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 249, lines 17–24).
[^139]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 265, lines 8–15).
[^140]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 265, lines 13–20).
[^141]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 275, lines 10–17).
[^142]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 276, lines 33–40).
[^143]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 289, lines 1–8).
[^144]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 262, lines 2–9).
[^145]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 262, lines 4–11).
[^146]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 248, lines 1–8).
[^147]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 289, lines 18–25).
[^148]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 267, lines 12–19).
[^149]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 292, lines 1–8).
[^150]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 329, lines 1–1).
[^151]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 397, lines 1–1).
[^152]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 437, lines 1–1).
[^153]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 329, lines 1–25).
[^154]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 336, lines 4–11).
[^155]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 340, lines 1–8).
[^156]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 381, lines 1–8).
[^157]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 355, lines 23–30).
[^158]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 350, lines 3–10).
[^159]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 336, lines 6–13).
[^160]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 339, lines 33–40).
[^161]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 363, lines 3–10).
[^162]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 360, lines 6–13).
[^163]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 362, lines 2–9).
[^164]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 386, lines 1–8).
[^165]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 360, lines 3–10).
[^166]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 362, lines 6–13).
[^167]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 373, lines 6–13).
[^168]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 366, lines 39–44).
[^169]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 397, lines 1–1).
[^170]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 437, lines 1–1).
[^171]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 485, lines 1–1).
[^172]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 397, lines 1–25).
[^173]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 428, lines 22–29).
[^174]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 433, lines 9–16).
[^175]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 427, lines 29–36).
[^176]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 431, lines 12–19).
[^177]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 403, lines 24–31).
[^178]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 403, lines 25–32).
[^179]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 416, lines 7–14).
[^180]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 426, lines 1–8).
[^181]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 399, lines 8–15).
[^182]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 397, lines 10–17).
[^183]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 407, lines 30–37).
[^184]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 398, lines 3–10).
[^185]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 433, lines 1–8).
[^186]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 401, lines 3–10).
[^187]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 401, lines 3–10).
[^188]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 437, lines 1–1).
[^189]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 485, lines 1–1).
[^190]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 539, lines 1–1).
[^191]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 437, lines 1–25).
[^192]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 440, lines 19–26).
[^193]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 468, lines 4–11).
[^194]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 444, lines 16–23).
[^195]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 461, lines 1–8).
[^196]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 461, lines 1–8).
[^197]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 479, lines 6–13).
[^198]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 470, lines 4–11).
[^199]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 465, lines 38–45).
[^200]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 441, lines 15–22).
[^201]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 444, lines 18–25).
[^202]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 460, lines 2–9).
[^203]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 440, lines 8–15).
[^204]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 482, lines 19–26).
[^205]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 478, lines 17–24).
[^206]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 442, lines 16–23).
[^207]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 485, lines 1–1).
[^208]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 539, lines 1–1).
[^209]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 565, lines 1–1).
[^210]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 485, lines 1–25).
[^211]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 533, lines 14–21).
[^212]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 485, lines 3–10).
[^213]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 520, lines 25–32).
[^214]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 522, lines 26–33).
[^215]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 485, lines 24–31).
[^216]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 491, lines 2–9).
[^217]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 491, lines 2–9).
[^218]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 538, lines 5–12).
[^219]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 485, lines 33–40).
[^220]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 501, lines 1–8).
[^221]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 516, lines 1–8).
[^222]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 492, lines 8–15).
[^223]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 493, lines 27–34).
[^224]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 522, lines 7–14).
[^225]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 524, lines 14–21).
[^226]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 539, lines 1–1).
[^227]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 565, lines 1–1).
[^228]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 597, lines 1–1).
[^229]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 539, lines 1–25).
[^230]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 546, lines 1–8).
[^231]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 564, lines 6–13).
[^232]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 547, lines 5–12).
[^233]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 544, lines 31–38).
[^234]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 544, lines 31–38).
[^235]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 559, lines 13–20).
[^236]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 560, lines 1–8).
[^237]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 561, lines 6–13).
[^238]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 546, lines 1–8).
[^239]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 549, lines 26–33).
[^240]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 561, lines 8–15).
[^241]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 561, lines 15–22).
[^242]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 547, lines 34–41).
[^243]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 545, lines 16–23).
[^244]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 548, lines 15–22).
[^245]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 565, lines 1–1).
[^246]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 597, lines 1–1).
[^247]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 565, lines 1–25).
[^248]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 594, lines 24–31).
[^249]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 578, lines 5–12).
[^250]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 565, lines 16–23).
[^251]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 578, lines 21–28).
[^252]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 578, lines 24–31).
[^253]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 578, lines 2–9).
[^254]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 592, lines 6–13).
[^255]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 590, lines 12–19).
[^256]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 567, lines 21–28).
[^257]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 574, lines 9–16).
[^258]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 589, lines 3–10).
[^259]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 589, lines 3–10).
[^260]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 586, lines 26–33).
[^261]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 578, lines 27–34).
[^262]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 570, lines 39–43).
[^263]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 597, lines 1–1).
[^264]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 597, lines 1–25).
[^265]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 642, lines 1–8).
[^266]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 696, lines 33–40).
[^267]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 599, lines 26–33).
[^268]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 699, lines 34–41).
[^269]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 674, lines 6–13).
[^270]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 690, lines 55–62).
[^271]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 690, lines 80–87).
[^272]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 597, lines 18–25).
[^273]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 611, lines 21–28).
[^274]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 606, lines 29–36).
[^275]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 611, lines 5–12).
[^276]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 686, lines 19–26).
[^277]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 686, lines 15–22).
[^278]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 624, lines 6–13).
[^279]: Beazley, David and Jones, Brian K.. *Python Cookbook, 3rd Edition*. (JSON `Python Cookbook 3rd.json`, p. 649, lines 5–12).
