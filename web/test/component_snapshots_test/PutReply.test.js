// Link.react.test.js
import React from 'react';
import Enzyme, { mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import renderer from 'react-test-renderer';
import Question from '../../src/Components/Question';

Enzyme.configure({ adapter: new Adapter() });

global.flushPromises = () => new Promise(resolve => setImmediate(resolve));

var sampleQuestionComponent = <Question
    question={{
        "_id": "id", "isAnonymous": true, "reply": "sample reply"
    }}
    adminSecret="secret"
/>


test('Reply button renders properly test', () => {
    const component = renderer.create(sampleQuestionComponent);
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
});



test('Reply workflow test', () => {
    global.fetch = jest.fn(() =>
        Promise.resolve({
            json: () => Promise.resolve({}),
            ok: true
        })
    );

    const wrapper = mount(sampleQuestionComponent);
    const expectedHtmlBeforeClick = '<div>sample reply</div>'
    const expectedHtmlAfterClick = '<div><form><textarea id="responseBox" class="response" name="question">sample reply</textarea><label for="responseBox"></label><input class="add-new-button" type="submit" value="Submit"></form></div>'
    expect(wrapper.html().includes(expectedHtmlBeforeClick)).toEqual(true);
    wrapper.find('[className="svg-inline--fa fa-reply fa-w-16 reply-button"]').simulate('click')
    expect(wrapper.html().includes(expectedHtmlAfterClick)).toEqual(true);
    wrapper.find('input.add-new-button').simulate('submit')

    return flushPromises().then(() => {
        expect(wrapper.html().includes(expectedHtmlBeforeClick)).toEqual(true);
        expect(wrapper.html().includes(expectedHtmlAfterClick)).toEqual(false);
    });

});




test('Reply workflow with error test', () => {

    global.fetch = jest.fn(() =>
        Promise.resolve({
            json: () => Promise.resolve({ 'message': 'wrong' }),
            ok: false
        })
    );
    const wrapper = mount(sampleQuestionComponent);
    wrapper.find('[className="svg-inline--fa fa-reply fa-w-16 reply-button"]').simulate('click')
    wrapper.find('input.add-new-button').simulate('submit')

    return flushPromises().then(() => {
        expect(wrapper.html().includes('wrong')).toEqual(true);
    });

});