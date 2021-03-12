// Link.react.test.js
import React from 'react';
import SurveyLink from '../../src/Components/SurveyLink';
import renderer from 'react-test-renderer';

document.execCommand = jest.fn()

test('Survey link renders properly test', () => {
  const component = renderer.create(
    <SurveyLink link="https://www.example.com"/>
  );
  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});

test('Survey link shows info about copied link', () => {
  const component = renderer.create(
      <SurveyLink link="https://www.example.com"/>
  );
  let tree = component.toJSON();

  // manually trigger the callback
  tree.props.onClick();
  // re-rendering
  tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});