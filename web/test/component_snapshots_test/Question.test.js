// Link.react.test.js
import React from 'react';
import Question from '../../src/Components/Question';
import renderer from 'react-test-renderer';


test('Question renders properly test', () => {
  const component = renderer.create(
    <Question 
      question={ {
        "_id": "id"
      }}
      handleVote={(_) => {return () => {};}}
      deleteQuestion={() => {}}
    />
  );
  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});