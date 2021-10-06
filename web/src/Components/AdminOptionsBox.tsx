import React, { FormEvent } from 'react';
import { decamelizeKeys } from 'humps';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import FormControl from '@material-ui/core/FormControl';

import { SURVEYS_API } from '../Consts';
import { TextField } from '@material-ui/core';

interface AdminOptionsProps {
    surveyKey: string;
    adminSecret: string;
    askingQuestionsEnabled: boolean;
    votingEnabled: boolean;
    limitQuestionCharactersEnabled: boolean;
    limitQuestionCharacters: number;
}

export default class AdminOptionsBox extends React.Component<AdminOptionsProps, any> {

    constructor(props: AdminOptionsProps) {
        super(props)
        this.state = {
            askingQuestionsEnabled: this.props.askingQuestionsEnabled,
            votingEnabled: this.props.votingEnabled,
            limitQuestionCharactersEnabled: this.props.limitQuestionCharactersEnabled,
            limitQuestionCharacters: this.props.limitQuestionCharacters
        }
        this.handleChange = this.handleChange.bind(this);
    }

    componentDidUpdate(prevProps: any) {
        if (prevProps !== this.props) {
            this.setState({
                askingQuestionsEnabled: this.props.askingQuestionsEnabled,
                votingEnabled: this.props.votingEnabled,
                limitQuestionCharactersEnabled: this.props.limitQuestionCharactersEnabled,
                limitQuestionCharacters: this.props.limitQuestionCharacters
            })
        }
    }

    handleChange = async (e: FormEvent<HTMLElement>) => {
        const setting: {[index: string]: any} = {}
        const target = e.target as HTMLInputElement;
        var value;
        switch(target.type) {
            case 'checkbox':
                value = target.checked;
                break;
            case 'number':
                value =  Number.parseFloat(target.value);
                break;
            default:
                value = target.value;

        }
        const name = target.name;
        this.setState({ [name]: value })
        setting[name] = value
        fetch(`${SURVEYS_API}${this.props.surveyKey}?admin_secret=${this.props.adminSecret}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(decamelizeKeys(setting))
        });
      }

    render(): JSX.Element {
        return (<div className="admin-box">
                <FormControl component="fieldset">
                    <FormGroup>
                        <FormControlLabel
                            control={
                            <Checkbox
                                checked={this.state.askingQuestionsEnabled}
                                onChange={this.handleChange} 
                                name="askingQuestionsEnabled"
                                color="primary" />
                            }
                            label="Asking Questions Enabled"/>
                        <FormControlLabel
                            control={
                            <Checkbox
                                checked={this.state.votingEnabled}
                                onChange={this.handleChange} 
                                name="votingEnabled"
                                color="primary" />
                            }
                            label="Voting Enabled"/>
                        <FormControlLabel
                            control={
                            <Checkbox
                                checked={this.state.limitQuestionCharactersEnabled}
                                onChange={this.handleChange} 
                                name="limitQuestionCharactersEnabled"
                                color="primary" />
                            }
                            label="Limit question length"/>
                        {
                            this.state.limitQuestionCharactersEnabled && <FormControlLabel
                                control={
                                <TextField
                                    value={this.state.limitQuestionCharacters}
                                    onChange={this.handleChange} 
                                    type="number"
                                    name="limitQuestionCharacters"
                                    color="primary"
                                    style={{
                                        width:((this.state.limitQuestionCharacters.toString().length + 1) * 12) + 'px'
                                    }} />
                                }
                                label="characters"/>
                        }
                    </FormGroup>
                </FormControl>
            </div>
        );
    }
}
