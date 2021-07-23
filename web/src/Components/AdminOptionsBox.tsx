import React, { FormEvent } from 'react';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';

import { SURVEYS_API } from '../Consts';

interface AdminOptionsProps {
    surveyKey: string;
    adminSecret: string;
    surveyStateCallback: any;
    allowAskingQuestions: boolean;
    allowVoting: boolean;
}

interface AdminOptionsState {
    allowAskingQuestions: boolean;
    allowVoting: boolean;
    errorMessage: string;
}

export default class AdminOptionsBox extends React.Component<AdminOptionsProps, AdminOptionsState> {

   handleSubmitAllowAskingQuestions = async (e: FormEvent<HTMLElement>) => {
        fetch(`${SURVEYS_API}${this.props.surveyKey}?admin_secret=${this.props.adminSecret}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({allowAskingQuestions: !this.props.allowAskingQuestions})
        })
        .then(async response => {
            let data = await response.json();
            this.props.surveyStateCallback(data.open);
        });
    };

    handleSubmitAllowVoting = async (e: FormEvent<HTMLElement>) => {
        fetch(`${SURVEYS_API}${this.props.surveyKey}?admin_secret=${this.props.adminSecret}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({allowVoting: !this.props.allowVoting})
        })
        .then(async response => {
            let data = await response.json();
            this.props.surveyStateCallback(data.open);
        });
    };

    render(): JSX.Element {
        return (<div className="admin-box">
                <FormControl component="fieldset">
                    {/* <FormLabel component="legend">Open to new questions</FormLabel> */}
                    <FormGroup>
                        <FormControlLabel
                            control={
                            <Checkbox
                                checked={this.props.allowAskingQuestions}
                                onChange={this.handleSubmitAllowAskingQuestions}
                                name="checkedB"
                                color="primary"
                            />
                            }
                            label={this.props.allowAskingQuestions ? 'Open for new questions' : 'Closed for questions (No new questions allowed)'}
                        />
                        <FormControlLabel
                            control={
                            <Checkbox
                                checked={this.props.allowVoting}
                                onChange={this.handleSubmitAllowAskingQuestions}
                                name="checkedB"
                                color="primary"
                            />
                            }
                            label={this.props.allowVoting ? 'Open (Questions and voting allowed)' : 'Closed (No new questions or voting allowed)'}
                        />
                    </FormGroup>
                </FormControl>
            </div>
        );
    }
}
