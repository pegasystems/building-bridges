import React from 'react';
import * as Models from '../Models'
import {SURVEYS_API, QUESTIONS_ENDPOINT} from '../Consts'
import Eye from './Eye';


export enum UserVote {
    Up = "up",
    Down = "down",
    None = "none",
}


export interface QuestionProps { 
    surveyKey: string;
    question: Models.Question;
    adminSecret: string | undefined;
    deleteQuestionCallback(question_id: string): void;
    addVoteCallback(question: Models.Question, voteType: Models.UserVote): any;
    deleteVoteCallback(question: Models.Question): any;
    markAsReadCallback(question: Models.Question): any;
    updateQuestionInState(question: Models.Question): any;
}

export default class Question extends React.Component<QuestionProps, {}> {

    deleteQuestion = (e: React.FormEvent<HTMLFormElement>) => {
        fetch(`${SURVEYS_API}${this.props.surveyKey}${QUESTIONS_ENDPOINT}/${this.props.question._id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                this.props.deleteQuestionCallback(this.props.question._id);
            }
        });
        e.preventDefault();
    };

    newVote(question: Models.Question, newVoteType: Models.UserVote)  {
        fetch(`${SURVEYS_API}${this.props.surveyKey}${QUESTIONS_ENDPOINT}/${question._id}/vote?type=${newVoteType}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                this.props.addVoteCallback(question, newVoteType);
            }
        });
    }

    deleteVote(question: Models.Question) {
        fetch(`${SURVEYS_API}${this.props.surveyKey}${QUESTIONS_ENDPOINT}/${question._id}/vote`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                this.props.deleteVoteCallback(question);
            }
        });
    }

    vote = (question: Models.Question, newVoteType: Models.UserVote, e: React.FormEvent<HTMLFormElement>) => {
        if (question.voted === newVoteType) {
            this.deleteVote(question);
        }
        else {
            this.newVote(question, newVoteType);
        }
        e.preventDefault();
    }

    markAsRead = (question: Models.Question, e: React.FormEvent<HTMLFormElement>) => {

        fetch(`${SURVEYS_API}${this.props.surveyKey}${QUESTIONS_ENDPOINT}/${question._id}/ctx?read=${question.read === 'true' ? 'false' : 'true'}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {     
                this.props.markAsReadCallback(Models.Question.createQuestionFromApiResult(question));
            }
        });

        e.preventDefault();
    }

    markAsHidden = () => {
        fetch(`${SURVEYS_API}${this.props.surveyKey}${QUESTIONS_ENDPOINT}/${this.props.question._id}?admin_secret=${this.props.adminSecret}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({hidden: !this.props.question.hidden})
        })
        this.props.question.hidden = !this.props.question.hidden;
        this.props.updateQuestionInState(this.props.question);
    };
    
    render(): JSX.Element {
        const question = this.props.question;
        const deleteButton = question.isAuthor && !this.props.adminSecret && (question.upvotes + question.downvotes === 0 || question.hideVotes) ?
            <form onSubmit={this.deleteQuestion}>
            <input type="hidden" name="id" value={question._id}/>
            <input type="submit" value="x" title="Remove this question" className="remove"/>
            </form> :
            <div/>;
        const hideButton = this.props.adminSecret ?
            <Eye slashed={this.props.question.hidden} hideOrShowCallback={this.markAsHidden}></Eye>
            : <div/>;
        const questionReadMarker = question.read === 'true' ? 'read' : ''
        const userVote = question.voted !== 'none' ? question.voted : questionReadMarker
        return (<li className={'vote ' + (this.props.adminSecret ? "" : userVote) + (this.props.question.hidden ? 'hidden' : '')} id={question._id}>
            <div className="right">
                <div className="thumbs">
                    <div className="item">
                        <form onSubmit={e => this.vote(question, Models.UserVote.Up, e)}>
                            <input type="hidden" name="id" value={question._id}/>
                            <input className="submit-up" type="submit" value={!question.hideVotes ? question.upvotes : ''}/>
                        </form>
                    </div>
                    <div className="item">
                        <form onSubmit={e => this.vote(question, Models.UserVote.Down, e)}>
                            <input type="hidden" name="id" value={question._id}/>
                            <input className="submit-down" type="submit" value={!question.hideVotes ? question.downvotes : ''}/>
                        </form>
                    </div>
                    <div className={'mark-as-read item ' + (question.read === 'true' ? 'read' : '')}>
                        <form onSubmit={e => this.markAsRead(question, e)}>
                            <input type="hidden" name="id" value={question._id}/>
                            <input title={'Mark as ' + (question.read === 'true' ? 'unread' : 'read')}
                                   className="submit-read" type="submit" value=""/>
                        </form>
                    </div>
                </div>
            </div>
            <div className="center">{question.content}</div>
            <a href={`#${question._id}`} title="Direct link to this post" className="permalink">#</a>
            {deleteButton}
            {hideButton}
        </li>);
    }
}
