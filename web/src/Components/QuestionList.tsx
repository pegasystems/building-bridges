import React from 'react';
import Question from "./Question" 
import * as Models from '../Models'
import QuestionModel from '../Models/Question';

interface QuestionListProps {
    questions: Models.Question[];
    sort: boolean;
    header: string;
    enumerate: boolean;
    voted: boolean;
    functions: any;
    surveyKey: string;
    isResultPage: boolean;
    adminSecret: string | undefined;
    open: boolean;
}

export default class QuestionList extends React.Component<QuestionListProps, {}> {

    doNothingFunction = (_: any) => (__: any) => (e: any) => {e.preventDefault();};

    sortQuestion(lhs: QuestionModel, rhs: QuestionModel): number {
        if (lhs.hidden !== rhs.hidden) {
            return +lhs.hidden - +rhs.hidden;
        }
        return (rhs.upvotes - rhs.downvotes) - (lhs.upvotes - lhs.downvotes)
    }

    render(): JSX.Element {
        let questions = this.props.questions;
        if (questions) {
            if (this.props.sort) {
                questions = questions.sort(this.sortQuestion);
            }

            const surveyElements = questions
                .map(question => {
                    let {deleteQuestion, addVoteCallback, deleteVoteCallback, markAsReadCallback, updateQuestionInState} = this.props.functions;
                    if (!this.props.open || this.props.isResultPage) {
                        deleteQuestion = this.doNothingFunction;
                        addVoteCallback = this.doNothingFunction;
                        deleteVoteCallback = this.doNothingFunction;
                        markAsReadCallback = this.doNothingFunction;
                    }
                    if (this.props.isResultPage) {
                        question.voted = Models.UserVote.None;
                    }
                    
                    return (
                        <Question surveyKey={this.props.surveyKey}
                                  question={question}
                                  addVoteCallback={addVoteCallback}
                                  deleteQuestionCallback={deleteQuestion}
                                  deleteVoteCallback={deleteVoteCallback}
                                  markAsReadCallback={markAsReadCallback}
                                  adminSecret={this.props.adminSecret}
                                  updateQuestionInState={updateQuestionInState}
                                  key={question._id}/>
                    );
                });
            return (
                <div className={this.props.header}>
                    <div className="voted-unvoted-header">
                        <h4>{this.props.header}</h4>
                    </div>
                    <ul className={this.props.enumerate ? 'enumerate' : ""} id={this.props.voted ? 'voted' : ""}>
                        {surveyElements}
                    </ul>
                </div>
            );
        }

        return (<></>);
    }
}