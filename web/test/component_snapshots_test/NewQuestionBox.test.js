import Enzyme, {mount} from "enzyme";
import renderer from "react-test-renderer";
import NewQuestionBox from "../../src/Components/NewQuestionBox";
import React from "react";
import Adapter from "enzyme-adapter-react-16";

Enzyme.configure({ adapter: new Adapter() });

global.flushPromises = () => new Promise(resolve => setImmediate(resolve));

global.fetch = jest.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve({
            userFullName: "John Doe",
            userEmail: "john.doe@company.com"
        })
    })
);

test('NewQuestionBox renders properly test', () => {
    const component = renderer.create(
        <NewQuestionBox surveyKey='survey-1' isAnonymous={true}/>
);
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
});

test('NewQuestionBox shows disclaimer about lack of anonymity when isAnonymous set to false', () => {
    const wrapper = mount(
        <NewQuestionBox surveyKey='survey-1' isAnonymous={false}/>
    );
    return flushPromises().then(() => {
        wrapper.update();
        expect(wrapper.contains(<h5>The survey is not anonymous -
        your question will be attributed to John Doe (john.doe@company.com).</h5>)).toEqual(true);
    });
});

test('NewQuestionBox does not show disclaimer about lack of anonymity when isAnonymous set to true', () => {
    const wrapper = mount(
        <NewQuestionBox surveyKey='survey-1' isAnonymous={true}/>
);
    return flushPromises().then(() => {
        wrapper.update();
        expect(wrapper.contains(<h5>The survey is not anonymous -
        your question will be attributed to John Doe (john.doe@company.com).</h5>)).toEqual(false);
    });
});


