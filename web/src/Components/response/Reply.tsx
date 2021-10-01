import React, { FormEvent } from 'react';
import './Reply.css'
import * as Consts from '../../Consts'
import Question from '../Question';
import QuestionModel from '../../Models/Question';

interface ReplyProps {
    editMode: boolean;
    question: Question;
    questionModel: QuestionModel
}

interface ReplyState {
    newResponseContent: string;
    errorMessage: string;
}

export default class Reply extends React.Component<ReplyProps, ReplyState> {

    constructor(props: ReplyProps) {
        super(props);
        this.state = {
            newResponseContent: props.questionModel.reply,
            errorMessage: ''
        }
    }

    handleSubmit = async (e: FormEvent<HTMLElement>) => {
        fetch(`${Consts.SURVEYS_API}${this.props.question.props.surveyKey}/questions/${this.props.question.props.question._id}${Consts.REPLIES_ENDPOINT}?admin_secret=${this.props.question.props.adminSecret}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: this.state.newResponseContent
            })
        })
            .then(async response => {
                let data = await response.json();
                if (!response.ok) {
                    this.setState({ errorMessage: data['message'] })
                }
                else {
                    this.props.questionModel.reply = this.state.newResponseContent;
                    this.props.question.switchDisplayReplyField();
                }
            });
        e.preventDefault();
    };

    handleResponseContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        this.setState({
            newResponseContent: e.target.value,
        });
    };

    render(): JSX.Element {
        let responseForm = (<form onSubmit={this.handleSubmit}>
            <textarea
                id="responseBox"
                className="response"
                name="question"
                value={this.state.newResponseContent}
                onChange={this.handleResponseContentChange} />
            <label htmlFor="responseBox">{this.state.errorMessage}</label>
            <input className="add-new-button"
                type="submit"
                value="Submit" />
        </form>)
        let content = this.props.editMode ? <div>{responseForm}</div> : <div>{this.state.newResponseContent}</div>
        return (this.state.newResponseContent || this.props.editMode ? <div className="response">
            {content}
            <div className="footnote">Answered by survey admin</div>
        </div> : <div />)
    }
}