import React, { FormEvent } from 'react';
import * as Models from '../Models'
import * as Consts from '../Consts'
import {SURVEYS_API} from "../Consts";
import {shuffle} from "../utils";

interface NewQuestionBoxProps {
    surveyKey: string;
    questionAuthorNameFieldVisible: boolean,
    limitQuestionCharactersEnabled: boolean,
    limitQuestionCharacters: number,
    isAnonymous: boolean;
    afterSubmit(question: Models.Question): any
}

interface NewQuestionBoxState {
    newQuestionContent: string;
    authorNickname: string;
    errorMessage: string;
    userFullName: string;
    userEmail: string;
}

export default class NewQuestionBox extends React.Component<NewQuestionBoxProps, NewQuestionBoxState> {
    state = {
        newQuestionContent: "",
        numberOfCharacters: 0,
        errorMessage: "",
        userFullName: "",
        userEmail: "",
        authorNickname: ""
    }

    componentDidMount() {
        this.getUserInfo();
    }

    getUserInfo() {
        var fetchUrl = `/api/info/whoami`

        fetch(fetchUrl)
            .then(response => {
                return response.json();
            }).then(data => {
            this.setState({...data});
        });
    }

   handleSubmit = async (e: FormEvent<HTMLElement>) => {
        fetch(`${Consts.SURVEYS_API}${this.props.surveyKey}${Consts.QUESTIONS_ENDPOINT}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: this.state.newQuestionContent,
                author_nickname: this.state.authorNickname
            })
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
                question.isAnonymous = this.props.isAnonymous;
                question.authorFullName = this.state.userFullName;
                question.authorEmail = this.state.userEmail;
                question.authorNickname=this.state.authorNickname;
                this.setState({newQuestionContent: ''});
                this.setState({newQuestionContent: ''});
                this.props.afterSubmit(question);
            }
            });
        e.preventDefault();
    };

    handleQuestionContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        if (this.props.limitQuestionCharactersEnabled && e.target.value.length > this.props.limitQuestionCharacters) {
            this.setState({
                errorMessage: "You've met this survey's character limit."
            })
            if (this.state.newQuestionContent.length == this.props.limitQuestionCharacters) {
                return
            }
        } else {
            this.setState({
                errorMessage: ''
            });
        }

        this.setState({
            newQuestionContent: e.target.value,
        });
    };

    handleQuestionContentPaste = (e: React.ClipboardEvent<HTMLTextAreaElement>) => {
        this.setState({
            newQuestionContent: e.clipboardData.getData('Text'),
        });
    };

    handleQuestionAuthorChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({
            authorNickname: e.target.value,
            errorMessage: ''
        });
    };

    render(): JSX.Element {
        let lackOfAnonymityDisclaimer = <div/>
        if (this.props.isAnonymous) {
            if (this.props.questionAuthorNameFieldVisible) {
                lackOfAnonymityDisclaimer = <div><h5>Name (optional): <input 
                    type="text" 
                    id="questionAuthor" 
                    value={this.state.authorNickname} 
                    onChange={this.handleQuestionAuthorChange}
                    maxLength={40}/></h5></div>
            }
        } else {
            lackOfAnonymityDisclaimer = <h5>The survey is not anonymous - your question will be attributed
            to {this.state.userFullName} ({this.state.userEmail}).</h5>
        }
        return (
            <div className="question-box">
                <h4>Ask a question</h4> 
                {
                    this.props.limitQuestionCharactersEnabled && 
                        <span
                            style={{
                                color: this.state.newQuestionContent.length > this.props.limitQuestionCharacters ? 'red' : 'black'
                            }}
                        >{this.state.newQuestionContent.length} of {this.props.limitQuestionCharacters}</span>
                }
                <form onSubmit={this.handleSubmit}>
                    <textarea 
                        id="questionBox" 
                        name="question" 
                        value={this.state.newQuestionContent}
                        onChange={this.handleQuestionContentChange}
                        onPaste={this.handleQuestionContentPaste}/>
                    <label htmlFor="questionBox">{this.state.errorMessage}</label>
                    {lackOfAnonymityDisclaimer}
                    <input className="add-new-button" 
                        type="submit" 
                        value="Submit"
                        disabled={this.props.limitQuestionCharactersEnabled && 
                            this.state.newQuestionContent.length > this.props.limitQuestionCharacters}/>
                </form>
            </div>
        );
    }
}
