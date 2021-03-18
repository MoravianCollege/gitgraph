
## Motivation

I wanted to create visualizations of a git history similar to those
in the [Git Book](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell).
I found a [StackOverflow question](https://stackoverflow.com/questions/1057564/pretty-git-branch-graphs)
that gave multiple ways to create graphics, and one of them is 
[gitdags](https://github.com/jubobs/gitdags), a LaTeX package.

This tool uses `gitdags` to automatically generate a graphic visualizing
the history of a repo.  It is "dumb" because sometimes the branch tags
overlap the commit hashes.  The tool will generate the `.tex` file, and you
can edit to fix this issue.

## Requirements

* `gitPython`[https://gitpython.readthedocs.io/en/stable/index.html]
* `pdflatex` - On a Mac, I suggest [MacTex](http://www.tug.org/mactex/)
* [`gitdags`](https://github.com/jubobs/gitdags).  The `.sty` file must be 
accessible.  If you installed MacTex, you can put the `.sty` in
`~/Library/texmf/tex/latex`
