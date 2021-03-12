import React from 'react';
import Question from "./Question" 
import * as Models from '../Models'

interface QuestionListProps {
    questions: Models.Question[];
    sort: boolean;
    header: string;
    enumerate: boolean;
    voted: boolean;
    functions: any;
    surveyKey: string;
    isResultPage: boolean;
}

export default class QuestionList extends React.Component<QuestionListProps, {}> {

    doNothingFunction = (_: any) => (__: any) => (e: any) => {e.preventDefault();};

    render(): JSX.Element {
        let questions = this.props.questions;
        if (questions) {
            if (this.props.sort) {
                questions = questions.sort((a, b) => (b.upvotes - b.downvotes) - (a.upvotes - a.downvotes));
            }

            const surveyElements = questions
                .map(question => {
                    let {deleteQuestion, addVoteCallback, deleteVoteCallback, markAsReadCallback} = this.props.functions;
                    if (this.props.isResultPage) {
                        question.voted = Models.UserVote.None;
                        deleteQuestion = this.doNothingFunction;
                        addVoteCallback = this.doNothingFunction;
                        deleteVoteCallback = this.doNothingFunction;
                        markAsReadCallback = this.doNothingFunction;
                    }
                    
                    return (
                        <Question surveyKey={this.props.surveyKey}
                                  question={question}
                                  addVoteCallback={addVoteCallback}
                                  deleteQuestionCallback={deleteQuestion}
                                  deleteVoteCallback={deleteVoteCallback}
                                  markAsReadCallback={markAsReadCallback}
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