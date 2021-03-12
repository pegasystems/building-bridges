import React from 'react';
import SurveyLink from './SurveyLink';
import * as Models from '../Models'

interface SurveyListProps {
    surveys: Models.Survey[];
}

interface SurveyListState {
    initSurveyKeys: string[]
}

export default class SurveyList extends React.Component<SurveyListProps, SurveyListState> {

    state = {
        initSurveyKeys: [] as string[]
    }

    componentDidMount(): void {
        this.setState((state, props) => ({initSurveyKeys:  props.surveys.map(survey => survey.key)}));
    }

    render(): JSX.Element {
        const surveyElements = this.props.surveys.map(survey => {
            const surveyUrl = `surveys/${survey.key}`;
            return (
                <tr className={this.state.initSurveyKeys.includes(survey.key) ? '' : 'new'} key={survey.key}>
                    <td>
                        <a href={surveyUrl}>{survey.title}</a>
                    </td>
                    <td className="fixed aligned-center">
                        {survey.viewsNumber}
                    </td>
                    <td className="fixed aligned-center">
                        {survey.questionersNumber}
                    </td>
                    <td className="fixed aligned-center">
                        {survey.votersNumber}
                    </td>
                    <td className="fixed aligned-center">
                        {new Date(survey.date).toLocaleString()}
                    </td>
                    <td className="fixed">
                        <SurveyLink link={`${window.location.href}${surveyUrl}`}/>
                    </td>
                    <td className="fixed">
                        <a href={`${surveyUrl}?results_secret=${survey.results_secret}`}>Show results</a>
                    </td>
                    <td className="fixed">
                        <a href={`${surveyUrl}?admin_secret=${survey.admin_secret}`}>Admin (Don't share this link)</a>
                    </td>
                </tr>
            );
        });

        if (surveyElements.length) {
            return (
                <div className="survey-list">
                    <table className="table survey-list">
                        <thead>
                        <tr>
                            <th colSpan={1}>
                                <h4>Your surveys</h4>
                            </th>
                            <th colSpan={1} className="aligned-center">
                                <h4>Unique visitors</h4>
                            </th>
                            <th colSpan={1} className="aligned-center">
                                <h4>Question authors</h4>
                            </th>
                            <th colSpan={1} className="aligned-center">
                                <h4>Voters</h4>
                            </th>
                            <th colSpan={1} className="aligned-center">
                                <h4>Created</h4>
                            </th>
                            <th colSpan={3}>
                            </th>
                        </tr>
                        </thead>
                        <tbody>
                        {surveyElements}
                        </tbody>
                    </table>
                </div>
            );
        }
        return <></>;
    }
}
