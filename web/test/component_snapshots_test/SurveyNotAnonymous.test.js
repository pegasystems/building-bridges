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


global.flushPromises = () => new Promise(resolve => setImmediate(resolve));

global.fetch = jest.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve({questions: [
                {_id: '1234', content: 'Question 1', upvotes: 1, downvotes: 0, isAuthor: true,
                    isAnonymous: false, authorFullName: "John Doe", authorEmail: "john.doe@company.com"},
                {_id: '1235', content: 'Question 2', upvotes: 0, downvotes: 1, isAuthor: false,
                    isAnonymous: false, authorFullName: "Jane Doe", authorEmail: "jane.doe@company.com"}
            ], key: 'survey-1', date: '2020-06-22', title: 'Survey test'})
    })
);

test('SurveyComponent contains question author info', () => {
    const wrapper = mount(
        <Survey match={{
        'params': {
            surveyKey: 'survey-1'
        }
    }} location={''}/>
);
    return flushPromises().then(() => {
        wrapper.update();
        expect(wrapper.contains(<a href="mailto:john.doe@company.com">John Doe</a>)).toEqual(true);
    });
});
