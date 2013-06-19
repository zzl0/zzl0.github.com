---
layout: post
title: Notes of Pro Git
---

#{{ page.title }}

<p class="meta">19 Jun 2013 - 长春</p>

This post records my thought when reading the book *Pro Git*

## Usefull Commands

1. git log --no-merges
2. git clone `<address>`
3. git fetch origin
4. git merge origin/master
5. git push origin master
6. git checkout `<branch_name>`


## Git Commit Guidelines

1. You don't want to submmit any whitespace errors. Using the following command:

		git diff --check

2. Try to make each commit a logically separate changeset.
3. Commit message. Here is a template originally written by Tim Pope at tpope.net:

		Capitalized, short (50 chars or less) summary

		More detailed explanatory text, if necessary.  Wrap it to about 72
		characters or so.  In some contexts, the first line is treated as the
		subject of an email and the rest of the text as the body.  The blank
		line separating the summary from the body is critical (unless you omit
		the body entirely); tools like rebase can get confused if you run the
		two together.

		Write your commit message in the imperative: "Fix bug" and not "Fixed bug"
		or "Fixes bug."  This convention matches up with commit messages generated
		by commands like git merge and git revert.

		Further paragraphs come after blank lines.

		- Bullet points are okay, too

		- Typically a hyphen or asterisk is used for the bullet, preceded by a
		  single space, with blank lines in between, but conventions vary here

		- Use a hanging indent

	The Git project has well-formatted commit message--run *git log --no-merges* there
	to see what a nicely formatted project-commit history looks like.


		
		
