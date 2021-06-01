import React from 'react';
import SurveyLink from '../../Components/SurveyLink';
import queryString from 'query-string';
import update from 'immutability-helper';
import Loader from 'react-loader-spinner';
import QuestionList from '../../Components/QuestionList';
import NewQuestionBox from '../../Components/NewQuestionBox';
import SurveyResultsInfo from '../../Components/SurveyResultsInfo';
import {SURVEYS_API, QUESTIONS_ENDPOINT} from '../../Consts'
import {shuffle} from '../../utils'
import * as Models from '../../Models';

import './Survey.css';

interface SurveyState {
    questions: Models.Question[];
    title: string;
    description: string;
    fetchInProgress: boolean;
    hideVotes: boolean;
    viewsNumber: number;
    questionersNumber: number;
    votersNumber: number;
    date: string;
    open: boolean;
}

interface SurveyProps {
    match: any;
    location: any;
}

export default class Survey extends React.Component<SurveyProps, SurveyState> {
    surveyKey: string;
    results_secret?: string | string[] | null;
    admin_secret?: string;

    constructor(props: SurveyProps) {
        super(props);
        this.state = {
            questions: [] as Models.Question[],
            fetchInProgress: true,
            title: '',
            description: '',
            hideVotes: false,
            viewsNumber: 0,
            questionersNumber: 0,
            votersNumber: 0,
            date: '',
            open: true
        };
        this.surveyKey = props?.match?.params?.surveyKey;
        this.results_secret = queryString.parse(props?.location?.search).results_secret?.toString();
        this.admin_secret = queryString.parse(props?.location?.search).admin_secret?.toString()
    }

    componentDidMount() {
        this.getQuestions();
    }

    getQuestions() {
        var fetchUrl = `${SURVEYS_API}${this.surveyKey}`

        if(this.results_secret) {
            fetchUrl += `?results_secret=${this.results_secret}`
        }
        if(this.admin_secret) {
            fetchUrl+=`${this.results_secret? '&' : '?'}admin_secret=${this.admin_secret}`
        }

        fetch(fetchUrl)
            .then(response => {
                if (response.status === 404 || response.status === 401) {
                    window.location.href = '/page404';
                }
                return response.json();
            }).then(data => {
            data.questions = shuffle(data.questions);
            data.questions = data.questions.map((questionDict: any) => {
                return Models.Question.createQuestionFromApiResult(questionDict);
            })
            this.setState({...data, ...{fetchInProgress: false}});
            if (window.location.hash) {
                window.location.href = window.location.hash;
            }
        });
    }

    deleteQuestionCallback = (_: string) => {
        this.getQuestions();
    }

    addQuestionToState = (question: Models.Question) => {
        if (this.state.hideVotes) {
            question.hideVotes = true;
        }
        this.setState(state => {
            return {questions: [question, ...state.questions]};
        });
        window.location.href = `#${question._id}`;
    }

    addVoteCallback = (question: Models.Question, voteType: Models.UserVote) => {
        if (this.state.hideVotes) {
            question.hideVotes = false;
            fetch(`${SURVEYS_API}${this.surveyKey}${QUESTIONS_ENDPOINT}/${question._id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.updateQuestionInState(data);
                });
        } else {
            question.addUserVote(voteType);
            this.updateQuestionInState(question);
        }
    }

    updateQuestionInState = (question: Models.Question) => {
        const questionIndex = this.state.questions.findIndex(q => q._id === question._id);
        this.setState({
            questions: update(this.state.questions, {
                [questionIndex]:
                    {$set: question}
            })
        });
    }

    updateSurveyStateCallback = (newState: boolean) => {
        this.setState({open: newState})
    }

    deleteVoteCallback = (question: Models.Question) => {
        let questionModel = Models.Question.createQuestionFromApiResult(question);
        if (this.state.hideVotes && questionModel.read === "false") {
            questionModel.hideVotes = true;
        } else {
            questionModel.removeUserVote();
        }
        questionModel.voted = Models.UserVote.None;
        this.updateQuestionInState(questionModel);
    }

    markAsReadCallback = (question: Models.Question) => {
        if (this.state.hideVotes) {
            question.hideVotes = false;
            fetch(`${SURVEYS_API}${this.surveyKey}${QUESTIONS_ENDPOINT}/${question._id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(data => {
                    question.toggleRead();
                    if (question.read === "false" && question.voted === Models.UserVote.None) {
                        data.upvotes = null
                    }
                    let newQuestionState = Models.Question.createQuestionFromApiResult(data);
                    this.updateQuestionInState(newQuestionState);
                });
        } else {
            question.toggleRead();
            this.updateQuestionInState(question);
        }
    }

    getQuestionsLists() {
        const questionFunctions = {
            deleteQuestion: this.deleteQuestionCallback,
            addVoteCallback: this.addVoteCallback,
            deleteVoteCallback: this.deleteVoteCallback,
            markAsReadCallback: this.markAsReadCallback,
            updateQuestionInState: this.updateQuestionInState
        };

        let questionsLists;
        if (this.showSingleColumn()) {
            const header = !this.showNewQuestionBox() ? 'Results' : '';
            questionsLists =
                <QuestionList questions={this.state.questions}
                              functions={questionFunctions}
                              header={header}
                              enumerate={true}
                              sort={true}
                              voted={true}
                              surveyKey={this.surveyKey}
                              isResultPage={this.showResultsSummary()}
                              adminSecret={this.admin_secret}
                              open={this.state.open}
                />;
        } else {
            questionsLists =
                <>
                    <QuestionList
                        questions={this.state.questions.filter(q => !q.hideVotes)}//q => q.voted !== Models.UserVote.None)}
                        functions={questionFunctions}
                        sort={true}
                        header="Voted questions"
                        voted={true}
                        enumerate={true}
                        surveyKey={this.surveyKey}
                        isResultPage={false}
                        adminSecret=''
                        open={this.state.open}
                    />

                    <QuestionList
                        questions={this.state.questions.filter(q => q.hideVotes)}//q => q.voted === Models.UserVote.None)}
                        functions={questionFunctions}
                        sort={false}
                        header="Unvoted questions"
                        voted={false}
                        enumerate={false}
                        surveyKey={this.surveyKey}
                        isResultPage={false}
                        adminSecret=''
                        open={this.state.open}
                    />
                </>;
        }
        return questionsLists;
    }

    private showSingleColumn() {
        return this.admin_secret || this.results_secret || !this.state.open || !this.state.hideVotes;
    }

    render(): JSX.Element {
        return (
            <div className={(this.state.hideVotes && this.state.open) ? 'hide-votes' : 'not-hide'}>
                <div className="title-div">
                    <h1 className="survey-title">{this.state.title}</h1>
                    <h1 className="survey-description">{this.state.description}</h1>
                    <SurveyLink link={document.location.href}/>
                    {!this.state.open && !this.admin_secret &&
                        <div className='results-info'>
                            <div className='aligned-center'>
                                This survey has been locked by the Survey Administrator. No new questions or votes can be submitted at this time.
                            </div>
                        </div>
                    }
                </div>
                <div>
                    {this.showResultsSummary() &&
                        <SurveyResultsInfo adminSecret={this.admin_secret} 
                                            surveyKey={this.surveyKey} 
                                            viewsNumber={this.state.viewsNumber}
                                            questionersNumber={this.state.questionersNumber}
                                            votersNumber={this.state.votersNumber} date={this.state.date} 
                                            open={this.state.open}
                                            surveyStateCallback={this.updateSurveyStateCallback}/>

                    }
                    {this.showNewQuestionBox() &&
                        <NewQuestionBox surveyKey={this.surveyKey} afterSubmit={this.addQuestionToState}/>
                    }
                </div>
                <div className="responses">
                    {
                        this.state.fetchInProgress ? <Loader type="TailSpin" color="#000000" height={80} width={80}/> :
                            this.getQuestionsLists()
                    }
                </div>
            </div>
        );
    }

    private showResultsSummary(): boolean {
        return Boolean(this.results_secret || this.admin_secret);
    }

    private showNewQuestionBox() {
        return !this.results_secret && !this.admin_secret && this.state.open;
    }
}
