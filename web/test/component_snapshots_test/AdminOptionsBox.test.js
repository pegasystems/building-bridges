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
            open={true} 
            surveyKey={'test_survey_key'} 
            adminSecret={'admin_secret'}
        />
    );
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
});

test('AdminOptions properly handle submit', () => {
    function callback(state) {
        try {
          expect(state).toBe(false);
          done();
        } catch (error) {
          done(error);
        }
    }
    const component = shallow(
        <AdminOptionsBox 
            open={true} 
            surveyKey={'test_survey_key'} 
            adminSecret={'admin_secret'}
            surveyStateCallback={callback}
        />
    );
    component.instance().handleSubmit('')
}); 
