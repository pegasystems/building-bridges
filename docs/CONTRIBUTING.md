# Contributing

## Workflow
1. File an issue to notify the maintainers about what you're working on.
2. Fork the repo, develop and test your code changes, add docs.
3. Make sure that your commit messages clearly describe the changes.
4. Send a pull request.



## Style Guides
1. Write in UTF-8 in Python 3
2. We follow [pep8](https://www.python.org/dev/peps/pep-0008/) standard when writing `python` code and [google style guide](https://google.github.io/styleguide/jsguide.html) for `javascript`
3. We use [Sonarqube](https://www.sonarqube.org/) for automatic Code Quality and Security scanning. Sonarqube won't let us merge Pull Request if it violets code quality rules.


## Make the Pull Request

Once you have made all your changes, tests, and updated the documentation,
make a pull request to move everything back into the main branch of the
`repository`. Be sure to reference the original issue in the pull request.
Expect some back-and-forth with regards to style and compliance of these
rules.


## Run Tests

To run tests, you can use `.scripts/runAllTests.sh`. You can see an information about your test code coverage locally - both xml and html files containing that information will be saved under *.sonar* directory.

## Run backend (api)

To run backend, you can run `python3 -m bridges` (or `./scripts/runBridges.sh` to set up environment). If you want to see which arguments can you use, type `python3 -m bridges -h`. The backend will default run on port 80, and **won't contain bridges website** (unless you run it in production environment, which means you have web files in *bridges/* directory). You should be able to go to `localhost:PORT/api`, to see *swagger* there - and you can test your api points in that place.

For more information about backend code, see [this document](BACKEND-CODE.md).

## Run frontend (website)

To run development website, you can execute: `npm start` in `web/` directory. This will run a development environment on port *3000*, and any changes in code in *web* will automatically in your browser, without need to run command again. Any api calls will go to port *8888*, so make sure your bridges BACKEND app is working on that port, if you want to use api calls. You can also change the API ENDPOINT in `web/src/setupProxy.js` to any URL that is hosting API points, so you don't have to run backend and database on your own, you can use a production one and just play with frontend.

Also, make sure that you have all *npm* packages installed before running website (`npm install` command).

For more information about frontend code, see [this document](FRONTEND-CODE.md).