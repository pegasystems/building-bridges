// Link.react.test.js
import React from 'react';
import SurveyResultsInfo from '../../src/Components/SurveyResultsInfo';
import renderer from 'react-test-renderer';


test('SurveyResultsInfo renders properly test', () => {
    const component = renderer.create(
        <SurveyResultsInfo
            surveyKey='dummyKey' viewsNumber={235}
            questionersNumber={13}
            votersNumber={34}/>
    );
    let tree = component.toJSON();
    expect(tree).toMatchSnapshot();
});