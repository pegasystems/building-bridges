import React from 'react';
import AdminOptionsBox from './AdminOptionsBox';
interface SurveyResultsInfoProps {
    date: string;
    surveyKey: string;
    viewsNumber: number;
    questionersNumber: number;
    votersNumber: number;
    adminSecret?: string;
    surveyStateCallback: any;
    open: boolean;
}

export default class SurveyResultsInfo extends React.Component<SurveyResultsInfoProps> {

    render(): JSX.Element {
        return (
            <div className='results-info'>
                <div className='aligned-center'>
                    This page is only for <strong>{this.props.adminSecret ? 'administration of your survey': 'viewing survey results'}</strong>. If you want to ask or vote on
                    questions, go to <a
                    href={'/surveys/' + this.props.surveyKey}>this page</a>. <br/><br/>
                    Here is some information about the survey engagement: <br/>
                </div>
                <table className='results-stats-table'>
                    <thead>
                    <tr>
                        <th className='aligned-center results-stats-table'>Unique visitors</th>
                        <th className='aligned-center results-stats-table'>Unique question authors</th>
                        <th className='aligned-center results-stats-table'>Unique voters</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td className='aligned-center results-stats-table'>{this.props.viewsNumber}</td>
                        <td className='aligned-center results-stats-table'>{this.props.questionersNumber}</td>
                        <td className='aligned-center results-stats-table'>{this.props.votersNumber}</td>
                    </tr>
                    </tbody>
                </table>
                {this.props.adminSecret && 
                    <AdminOptionsBox open={this.props.open} 
                                     surveyStateCallback={this.props.surveyStateCallback} 
                                     surveyKey={this.props.surveyKey} 
                                     adminSecret={this.props.adminSecret}/>
                }
            </div>
        );
    }
}
