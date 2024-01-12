
<div align="center">

### Identifying Dead Code in Java Programs with Call Graphs: a Comparative Study of Semantic and Syntactic Approaches

[![Report][report-shield]][report-url]
[![Presentation][presentation-shield]][presentation-url]

</div>


## Introduction
In the last 4 weeks of the course, we were challenge to put in practice the knowledge we had acquired, by developing a project and submitting a report according to the IEEE format.

Even though the project topic was quite broad, it was important that we showed competences, and demonstrated knowledge, in all the different analyses techniques covered in class.

## What's done
In one sentence, we set up ourselves to answer the following question:

> Considering accuracy, speed and complexity: is semantic analysis better than syntactic analysis for creating call graphs in Java programs to identify dead code?

### Idea
We decided to build our project around the idea of comparing 2 different analysis techniques: semantic and syntactic. Our comparison was based on 3 metrics: **accuracy**, **performance** and **complexity**. We compare the benchmark of these two techniques for a tool that can generate a call graph. Furthermore, other techniques - such as concolic execution, and syntactic analysis through the use of regular expressions - are discussed.

For a better idea of what we set up to do, the abstract of our report provides a good summary.

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


## Try on your machine?
Unfortunately if you try to run the code, it will fail because of problems with the paths. To fix this problem and organise the repository correctly, it would require some time. Ultimately, at this point, doing this wouldn't make sense. Maybe in the future... :cactus:



[python-shield]: https://img.shields.io/badge/Python-306998?style=for-the-badge&amp;logo=python&amp;logoColor=white
[antlr-url]: https://www.antlr.org/

<!--
[java-shield]: https://img.shields.io/badge/java-EC2025?style=for-the-badge&logoColor=white
[java-url]: ???
-->

[java-shield]: https://img.shields.io/badge/Java-EC2025?style=for-the-badge
[java-url]: https://www.java.com/

[treesitter-shield]: https://img.shields.io/badge/tree%20sitter-7E8F31?style=for-the-badge&logoColor=white
[treesitter-url]: https://tree-sitter.github.io/tree-sitter/

[jvm2json-shield]: https://img.shields.io/badge/jvm2json-000000?style=for-the-badge&logoColor=white
[jvm2json-url]: https://gitlab.gbar.dtu.dk/chrg/jvm2json

[presentation-shield]: https://img.shields.io/badge/presentation-555?style=for-the-badge&logoColor=black
[presentation-url]: https://github.com/immarianaas/pa-23/blob/master/project/presentation.pdf

[report-shield]: https://img.shields.io/badge/report-555?style=for-the-badge&logoColor=black
[report-url]: https://github.com/immarianaas/pa-23/blob/master/project/report.pdf

[example-shield]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[example-url]: https://getbootstrap.com/
