digraph {
	A [label="./course-02242-examples/src/dependencies/java/dtu/deps/tricky/Tricky.java"]
	C [label="dtu.deps.simple.*"]
	C -> A
	B [label=Tricky]
	B -> A
	D [label="dtu.deps.tricky"]
	D -> C
}
