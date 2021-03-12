import SurveyList from '../../src/Components/SurveyList';
import React from 'react';
import Adapter from 'enzyme-adapter-react-16';
import renderer from 'react-test-renderer';


test('SurveyList renders properly test', () => {
    const component = renderer.create(
        <SurveyList surveys={[{
            date: '2020-01-26T13:51:50.417Z',
            hideVotes: true,
            key: 'title-1',
            results_secret: 'cf9ff3424c90759a',
            admin_secret: 'cf9ff3424c90759b',
            title: 'title'
        }]}
        />
    );
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
});
