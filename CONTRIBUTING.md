# How to contribute

Thanks for helping this library! I'm hoping to keep it open-source and extensible for all applications and needs.

Some Resources:
  * Bugs or Feature Requests? Head to our [Github Issues](https://github.com/ereoh/papersummary/issues).
  * Questions? Check out our [Discussions Page](https://github.com/ereoh/papersummary/discussions).

## Testing

Please add the appropriate pytests for any new code you create.

## Submitting changes

Please send a [GitHub Pull Request](https://github.com/ereoh/papersummary/pull/new/maim) with a clear list of what you've done (read more about [pull requests](http://help.github.com/pull-requests/)).
> Please make sure your code follows to standards (below) and the PR is atomic (aka one feature).

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

    $ git commit -m "A brief summary of the commit
    > 
    > A paragraph describing what changed and its impact."

## Coding conventions

I mostly follow the [PEP 8](https://peps.python.org/pep-0008/) style guide (see code for examples). Use pylint and black to help clean up your code:

```bash
pylint papersummary
black papersummary tests
```

Cheers,
Ere Oh
