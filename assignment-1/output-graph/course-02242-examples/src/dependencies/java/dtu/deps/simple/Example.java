digraph {
	A [label="./course-02242-examples/src/dependencies/java/dtu/deps/simple/Example.java"]
	C [label="dtu.deps.util.Utils"]
	C -> A
	B [label=Other]
	B -> A
	D [label="dtu.deps.simple"]
	D -> C
}
