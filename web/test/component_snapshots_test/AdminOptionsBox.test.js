import AdminOptionsBox from '../../src/Components/AdminOptionsBox';
import React from 'react';
import renderer from 'react-test-renderer';
import Enzyme, { shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

Enzyme.configure({ adapter: new Adapter() });

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ok: 'true'}),
  })
);

test('AdminOptions renders properly test', () => {
    const component = renderer.create(
        <AdminOptionsBox 
            askingQuestionsEnabled={true} 
            votingEnabled={true} 
            surveyKey={'test_survey_key'} 
            adminSecret={'admin_secret'}
        />
    );
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
});

test('AdminOptions properly handle submit', () => {
    const formEventMocked = { target: <HTMLInputElement 
      type='checkbox'
      name='askingQuestionsEnabled'
      checked={false}/> }
    const component = shallow(
        <AdminOptionsBox 
            askingQuestionsEnabled={true} 
            votingEnabled={true} 
            surveyKey={'test_survey_key'} 
            adminSecret={'admin_secret'}
        />
    );
    component.instance().handleChange(formEventMocked)
}); 
