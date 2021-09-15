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

test('NewQuestionBox show counter when limit question characters set', () => {
    const wrapper = mount(
        <NewQuestionBox surveyKey='survey-1' limitQuestionCharactersEnabled={true} limitQuestionCharacters={10}/>
    );
    return flushPromises().then(() => {
        wrapper.update();
        expect(wrapper.html().includes('<span style="color: black;">0 of 10</span>')).toEqual(true);
    });
});

test('NewQuestionBox counter limit changes when content change', () => {
    const wrapper = mount(
        <NewQuestionBox surveyKey='survey-1' limitQuestionCharactersEnabled={true} limitQuestionCharacters={10}/>
    );
    wrapper.find('textarea').simulate('change', {target: { value: 'aa' }});
    return flushPromises().then(() => {
        wrapper.update();
        expect(wrapper.html().includes('<span style="color: black;">2 of 10</span>')).toEqual(true);
    });
});

test('NewQuestionBox counter limit changes when content change', () => {
    const wrapper = mount(
        <NewQuestionBox surveyKey='survey-1' limitQuestionCharactersEnabled={true} limitQuestionCharacters={5}/>
    );
    wrapper.find('textarea').simulate('change', {target: { value: '12345' }});
    wrapper.find('textarea').simulate('change', {target: { value: '123456' }});
    return flushPromises().then(() => {
        wrapper.update();
        expect(wrapper.html().includes('<span style="color: black;">5 of 5</span>')).toEqual(true);
        expect(wrapper.html().includes("You've met this survey's character limit.")).toEqual(true);
    });
});

test('NewQuestionBox should be able to paste overlimit content but not submit', () => {
    const wrapper = mount(
        <NewQuestionBox surveyKey='survey-1' limitQuestionCharactersEnabled={true} limitQuestionCharacters={5}/>
    );
    wrapper.find('textarea').simulate('change', {target: { value: '1234567' }});
    return flushPromises().then(() => {
        wrapper.update();
        expect(wrapper.html().includes('<span style="color: red;">7 of 5</span>')).toEqual(true);
    });
});

