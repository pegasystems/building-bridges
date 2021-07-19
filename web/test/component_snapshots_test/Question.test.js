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