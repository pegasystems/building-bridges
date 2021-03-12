import React, { FormEvent } from 'react';
import * as Models from '../Models'
import * as Consts from '../Consts'

interface NewQuestionBoxProps {
    surveyKey: string;
    afterSubmit(question: Models.Question): any
}

interface NewQuestionBoxState {
    newQuestionContent: string;
    errorMessage: string;
}

export default class NewQuestionBox extends React.Component<NewQuestionBoxProps, NewQuestionBoxState> {
    state = {
        newQuestionContent: "",
        errorMessage: ""
    }

   handleSubmit = async (e: FormEvent<HTMLElement>) => {
        fetch(`${Consts.SURVEYS_API}${this.props.surveyKey}${Consts.QUESTIONS_ENDPOINT}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({content: this.state.newQuestionContent})
        })
        .then(async response => {
            let data = await response.json();
            if (!response.ok) {
                this.setState({errorMessage: data['message']})
            }
            else {
                const question = new Models.Question();
                question._id = data._id;
                question.content = this.state.newQuestionContent;
                question.isAuthor = true;
                this.setState({newQuestionContent: ''});
                this.props.afterSubmit(question);
            }
            });
        e.preventDefault();
    };

    handleQuestionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        this.setState({
            newQuestionContent: e.target.value,
            errorMessage: ''
        });
    };

    render(): JSX.Element {
        return (
            <div className="question-box">
                <h4>Ask a question</h4>
                <form onSubmit={this.handleSubmit}>
                    <textarea id="questionBox" name="question" value={this.state.newQuestionContent}
                              onChange={this.handleQuestionChange}></textarea>
                    <label htmlFor="questionBox">{this.state.errorMessage}</label>
                    <input className="add-new-button" type="submit" value="Submit"/>
                </form>
            </div>
        );
    }
}
