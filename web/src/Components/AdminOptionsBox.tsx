import React, { FormEvent } from 'react';
import { decamelizeKeys } from 'humps';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import FormControl from '@material-ui/core/FormControl';

import { SURVEYS_API } from '../Consts';

interface AdminOptionsProps {
    surveyKey: string;
    adminSecret: string;
    askingQuestionsEnabled: boolean;
    votingEnabled: boolean;
}

export default class AdminOptionsBox extends React.Component<AdminOptionsProps, any> {

    constructor(props: AdminOptionsProps) {
        super(props)
        this.state = {
            askingQuestionsEnabled: this.props.askingQuestionsEnabled,
            votingEnabled: this.props.votingEnabled
        }
        this.handleChange = this.handleChange.bind(this);
    }

    componentDidUpdate(prevProps: any) {
        if (prevProps !== this.props) {
            this.setState({
                askingQuestionsEnabled: this.props.askingQuestionsEnabled,
                votingEnabled: this.props.votingEnabled
            })
        }
    }

    handleChange = async (e: FormEvent<HTMLInputElement>) => {
        const target = e.target as HTMLInputElement;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;
        this.setState({ [name]: value })
        const setting: {[index: string]: any} = {}
        setting[name] = target.checked
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
                    </FormGroup>
                </FormControl>
            </div>
        );
    }
}
