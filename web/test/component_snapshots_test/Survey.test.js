// Link.react.test.js
import React from 'react';
import Enzyme, { mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import Survey from '../../src/Pages/Survey/Survey';
import renderer from 'react-test-renderer';
import * as Models from '../../src/Models';

Enzyme.configure({ adapter: new Adapter() });

global.fetch = jest.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve({})
    })
);

test('SurveyComponent renders properly test', () => {
    const component = renderer.create(
        <Survey/>
    );
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
});


global.flushPromises = () => new Promise(resolve => setImmediate(resolve));

global.fetch = jest.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve({questions: [
                {_id: '1234', content: 'Question 1', upvotes: 1, downvotes: 0, isAuthor: true},
                {_id: '1235', content: 'Question 2', upvotes: 0, downvotes: 1, isAuthor: false}
            ], key: 'survey-1', date: '2020-06-22', title: 'Survey test'})
    })
);

test('SurveyComponent contains proper title test', () => {
    const wrapper = mount(
        <Survey match={{
            'params': {
                surveyKey: 'survey-1'
            }
        }} location={''}/>
    );
    return flushPromises().then(() => {
        wrapper.update();
        expect(wrapper.contains(<h1 className="survey-title">Survey test</h1>)).toEqual(true);
    });
});

test('Mark as read callback test', () => {
    const survey = new Survey();
    survey.state = {
        questions: [],
        fetchInProgress: true,
        title: '',
        hideVotes: false,
    };;
    survey.markAsReadCallback(Models.Question.createQuestionFromApiResult(
        {
            "content" : "content",
            "downvotes" : 0,
            "upvotes" : 0,
            "isAuthor" : 'true',
            "voted" : true,
            "_id" : "id",
            "read" : "false"
        }));

});