from git import Repo
import sys
import os


def short_hash(commit):
    return commit.hexsha[:7]


def get_first_commit(repo):
    for commit in repo.iter_commits():
        if commit.parents == ():
            return commit

    raise Exception('No commit without a parent!?!')


class GitDag:
    """
    This class computes the DAG for the commits in a git
    repo.  It can produce the tex representation of that DAG
    as expected by the gitdags LaTeX package
    """

    def __init__(self, repo_path):
        self.repo = Repo(repo_path)
        self.dag = self.make_dag()

    def make_dag(self):
        q = []
        for branch in self.repo.branches:
            commit = branch.commit
            q.append(commit)

        dag = {}

        while len(q) > 0:

            commit = q.pop()
            parents = commit.parents

            for parent in parents:

                if short_hash(parent) in dag:
                    add = False
                else:
                    add = True

                current = dag.get(short_hash(parent), set())
                current.add(short_hash(commit))
                dag[short_hash(parent)] = current
                if add:
                    q.append(parent)

        return dag

    def as_string(self):
        return self.as_string_helper(short_hash(get_first_commit(self.repo)))

    def as_string_helper(self, commit):

        ret = '{} --\n'.format(commit)
        if commit not in self.dag:
            return ret

        children = self.dag[commit]

        if len(children) == 1:
            return ret + self.as_string_helper(children.pop())
        else:
            ret += '{\n'
            for child in sorted(children):
                ret += self.as_string_helper(child)
                ret += ',\n'
            ret += '}'

        return ret


class GitGraph:
    def __init__(self, repo_path, filename='repo'):

        self.repo = Repo(repo_path)
        for branch in self.repo.branches:
            if '_' in branch.name:
                raise Exception('Underscore in branch name cannot render in pdflaex: {}'.format(branch.name))
        self.filename = filename
        self.dag = GitDag(repo_path)

    def make_graph(self):
        self.generate_tex()

    def generate_tex(self):
        file = open(self.filename + '.tex', 'w')
        print('\\documentclass{standalone}', file=file)
        print('\\usepackage{gitdags}', file=file)
        print('\\begin{document}', file=file)
        print('\\begin{tikzpicture}', file=file)
        print('\\gitDAG[grow right sep = 2em]{', file=file)
        print(self.dag.as_string(), file=file)
        print('};', file=file)
        referenced_commits = {}
        for branch in self.repo.branches:
            print('\\gitbranch', file=file)
            print('{', branch.name, '}', sep='', file=file)
            if branch.commit in referenced_commits:
                print('{right=of', referenced_commits[branch.commit], '}', file=file)
            else:
                print('{above=of', short_hash(branch.commit), '}', file=file)
                referenced_commits[branch.commit] = branch.name
            print('{', short_hash(branch.commit), '}', sep='', file=file)
        if self.repo.head.is_detached:
            head_name = short_hash(self.repo.head.commit)
        else:
            head_name = self.repo.head.reference.name
        print('\\gitHEAD', file=file)
        print('{above=of', head_name, '}', file=file)
        print('{', head_name, '}', sep='', file=file)
        print('\\end{tikzpicture}', file=file)
        print('\\end{document}', file=file)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <path to repo> [<image name>]".format(sys.argv[0]))
        sys.exit(1)
    repo_path = sys.argv[1]

    if len(sys.argv) == 3:
        filename = sys.argv[2]
    else:
        filename = 'repo'

    GitGraph(repo_path, filename).make_graph()
    print('Created {}.tex'.format(filename))

    os.system('pdflatex {}.tex > /dev/null 2>&1'.format(filename))
    #print('Created {}.pdf'.format(filename))
    os.system('sips -s format png {}.pdf --out {}.png > /dev/null 2>&1'.format(filename, filename))
    print('Created {}.png'.format(filename))
    os.system('rm {}.aux {}.log texput.log {}.pdf > /dev/null 2>&1'.format(filename, filename, filename))
