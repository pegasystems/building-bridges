import React from 'react';
import CreateSurvey from '../../src/Components/SurveyCreation';
import renderer from 'react-test-renderer';

global.fetch = jest.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve([{
            date: '2020-07-03',
            hideVotes: true,
            key: 'title-1',
            secret: 'cf9ff3424c90759a',
            title: 'title'
        },
        {
            date: '2020-07-04',
            hideVotes: false,
            key: 'title-2',
            secret: '89as8n97asdfkdf',
            title: 'title-2'
        }])
    })
);


test('CreateSurvey renders properly test', () => {
    const component = renderer.create(
        <CreateSurvey/>
    );
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
});


