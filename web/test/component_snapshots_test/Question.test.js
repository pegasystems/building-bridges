// Link.react.test.js
import React from 'react';
import Question from '../../src/Components/Question';
import renderer from 'react-test-renderer';


test('Question renders properly test', () => {
  const component = renderer.create(
    <Question 
      question={ {
        "_id": "id", "isAnonymous": true
      }}
      handleVote={(_) => {return () => {};}}
      deleteQuestion={() => {}}
    />
  );
  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});

test('Question with reply renders properly test', () => {
  const component = renderer.create(
    <Question 
      question={ {
        "_id": "id", "isAnonymous": true, "reply": "sample reply"
      }}
      handleVote={(_) => {return () => { /* This is intentional */ };}}
      deleteQuestion={() => { /* This is intentional */ }}
    />
  );
  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});

test('Not anonymous question renders properly test', () => {
    const component = renderer.create(
        <Question
    question={ {
        "_id": "id",
        "isAnonymous": false,
        "authorFullName": "John Doe",
        "authorEmail": "john.doe@company.com"
    }}
    handleVote={(_) => {return () => {};}}
    deleteQuestion={() => {}}
    />
);
    let tree = component.toJSON();
    expect(tree).toMatchSnapshot();
});