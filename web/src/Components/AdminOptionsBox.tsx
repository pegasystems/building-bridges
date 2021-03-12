import React, { FormEvent } from 'react';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';

import { SURVEYS_API } from '../Consts';

interface AdminOptionsProps {
    surveyKey: string;
    adminSecret: string;
    surveyStateCallback: any;
    open: boolean;
}

interface AdminOptionsState {
    open: boolean;
    errorMessage: string;
}

export default class AdminOptionsBox extends React.Component<AdminOptionsProps, AdminOptionsState> {

   handleSubmit = async (e: FormEvent<HTMLElement>) => {
        fetch(`${SURVEYS_API}${this.props.surveyKey}?admin_secret=${this.props.adminSecret}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({open: !this.props.open})
        })
        .then(async response => {
            let data = await response.json();
            this.props.surveyStateCallback(data.open);
        });
    };

    render(): JSX.Element {
        return (<div className="admin-box">
                <FormControl component="fieldset">
                    <FormLabel component="legend">Survey Status (toggle to Open or Close the survey)</FormLabel>
                    <FormGroup>
                        <FormControlLabel
                            control={
                            <Switch
                                checked={this.props.open}
                                onChange={this.handleSubmit}
                                name="checkedB"
                                color="primary"
                            />
                            }
                            label={this.props.open ? 'Open (Questions and voting allowed)' : 'Closed (No new questions or voting allowed)'}
                        />
                    </FormGroup>
                </FormControl>
            </div>
        );
    }
}
