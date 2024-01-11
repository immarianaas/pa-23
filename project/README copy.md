# Final project

## Introduction
In the last 4 weeks of the course, we were challenge to put in practice the knowledge we had acquired, by developing a project and submitting a report according to the IEEE format.

Even though the project topic was quite broad, it was important that we showed competences, and demonstrated knowledge, in all the different analyses techniques covered in class.

## What's done

### Idea
We decided to build our project around the idea of comparing 2 different analysis techniques: semantic and syntactic. For a better idea of what we set up to do, the abstract of our report provides a good summary.

> In this paper, we conduct a comparative analysis
of two static approaches aimed at identifying dead code in
Java programs. Our investigation involves a syntactic analysis
tool utilising parse trees, and an abstract interpreter that in-
terprets JVM bytecode. Both these tools strive to find an over-
approximation of all callable functions in a program. These are
then compared to each other to see which is performing best and
to a call graph created by running an interpreter on a program
with no parameters, which serves as the ground truth. We see
that both ways produce an over-approximation on the subset of
Java we handle, where the syntactic approach is faster, and the
semantic approach is closer to the ground truth. Despite it being
slower than the syntactic analysis, the semantic analysis should
be preferred due to the more precise result.

### Built with

<!--
- python
- java
- jvm2json
- tree-sitter
-->

[![Python][python-shield]][antlr-url] [![Java][java-shield]][java-url] [![Jvm2Json][jvm2json-shield]][jvm2json-url] [![Tree-sitter][treesitter-shield]][treesitter-url]


### :page_with_curl: Challenge
This exercise challenged us to solve the same problem as in the previous weeks - determine which inputs can lead functions to throw one of 4 exceptions. For this week, we were to develop this tool with a **dynamic analysis** point of view. In specific, using **concolic execution**.

Similarly to the last few weeks', this exercise was based on the analysis of Java bytecode, using the [jvm2json](https://gitlab.gbar.dtu.dk/chrg/jvm2json) tool.

The challenge is detailed on [Concolic-Execution.html](https://github.com/immarianaas/pa-23/blob/master/assignment-7/Concolic-Execution.html).

### :bar_chart: Results

No slide was created for this challenge, since the focus at this point was on starting working towards the course project.



[python-shield]: https://img.shields.io/badge/Python-306998?style=for-the-badge&amp;logo=python&amp;logoColor=white
[antlr-url]: https://www.antlr.org/

<!--
[java-shield]: https://img.shields.io/badge/java-EC2025?style=for-the-badge&logoColor=white
[java-url]: ???
-->

[java-shield]: https://img.shields.io/badge/Java-007CBD?style=for-the-badge
[java-url]: https://www.java.com/

[treesitter-shield]: https://img.shields.io/badge/tree%20sitter-7E8F31?style=for-the-badge&logoColor=white
[treesitter-url]: https://tree-sitter.github.io/tree-sitter/

[jvm2json-shield]: https://img.shields.io/badge/jvm2json-000000?style=for-the-badge&logoColor=white
[jvm2json-url]: https://gitlab.gbar.dtu.dk/chrg/jvm2json


[example-shield]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[example-url]: https://getbootstrap.com/
