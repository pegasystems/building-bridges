import React from 'react';
import * as Models from '../Models'

interface SurveyCreationState {
    newSurveyName: string;
    description: string;
    hideVotes: boolean;
    isAnonymous: boolean;
    canAddName: boolean;
    surveys: Models.Survey[];
}

interface SurveyCreationProps {
    addSurvey(survey: Models.Survey): void
}

export default class SurveyCreation extends React.Component<SurveyCreationProps, SurveyCreationState>  {

    state = {
        newSurveyName: '',
        description: '',
        hideVotes: false,
        isAnonymous: true,
        canAddName: false,
        surveys: [] as Models.Survey[]
    }

    handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        fetch('/api/surveys/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(
                {
                    title: this.state.newSurveyName,
                    description: this.state.description,
                    hideVotes: this.state.hideVotes,
                    isAnonymous: this.state.isAnonymous,
                    canAddName: this.state.canAddName
                }
            )
        })
        .then(response => response.json())
        .then(data => {
            const survey = new Models.Survey(
                data.key, this.state.newSurveyName, data.results_secret, data.admin_secret, 0, 0, 0
            );
            this.props.addSurvey(survey);
        })
        .catch(error => {
            console.error('Error:', error);
        });
        e.preventDefault();
    };

    handleSurveyNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({newSurveyName: e.target.value});
    };
    
    handleSurveyDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        this.setState({description: e.target.value});
    };

    handleHideVotesCheckBoxClick = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({
            hideVotes: e.target.checked,
        });
    }

    handleIsAnonymousCheckBoxClick = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({
            isAnonymous: !e.target.checked,
        });
    }

    handleCanAddNameCheckBoxClick = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({
            canAddName: e.target.checked,
        });
    }

    render(): JSX.Element {
        return (
            <div className="newSurveys" >
                <div className="new-survey-box">
                    <form id="createBridge" onSubmit={this.handleSubmit}>
                        <h4>Survey name</h4>
                        <div className="creation-flex">
                            <input className="survey-name" type="text" value={this.state.newSurveyName} 
                                onChange={this.handleSurveyNameChange} placeholder="Title of My Bridges Survey"
                                minLength={3}/>
                        </div>
                        <h4>Survey description</h4>
                        <div className="creation-flex">
                        <textarea className="survey-description" value={this.state.description} 
                                onChange={this.handleSurveyDescriptionChange} placeholder="Description (optional)"/>
                        </div>

                        <h4>Optional Features</h4>
                        <div className="options">
                            <label htmlFor="hide_votes" className="container-checkbox">Hide vote totals until after a user votes
                                <input type="checkbox" id="hide_votes" name="hide_votes" value={String(this.state.hideVotes)} onChange={this.handleHideVotesCheckBoxClick}/>
                                <span className="checkmark"></span>
                            </label>
                            <label htmlFor="show_names" className="container-checkbox">Show full names of question authors
                                <input type="checkbox" id="show_names" name="show_names" value={String(!this.state.isAnonymous)} onChange={this.handleIsAnonymousCheckBoxClick}/>
                                <span className="checkmark"></span>
                            </label>
                            {
                                this.state.isAnonymous && <label htmlFor="add_name" className="container-checkbox">Enable adding author name to question
                                    <input 
                                        type="checkbox" 
                                        id="add_name" 
                                        name="add_name" 
                                        value={String(this.state.canAddName)} 
                                        onChange={this.handleCanAddNameCheckBoxClick}/>
                                    <span className="checkmark"></span>
                                </label>
                            }
                        </div>
                        <input className="add-new-button" type="submit" value="Create survey" disabled={!this.state.newSurveyName}/>
                    </form>
                </div>
            </div>
        );
    }
}
