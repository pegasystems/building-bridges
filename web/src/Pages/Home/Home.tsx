import React from 'react';
import './Home.css';
import SurveyCreation from '../../Components/SurveyCreation';
import SurveyList from '../../Components/SurveyList';
import * as Models from '../../Models'

interface HomeState {
  surveys: Models.Survey[]
}

export default class Home extends React.Component<{}, HomeState> {

  state = {
    surveys: [] as Models.Survey[]
  }

  componentDidMount() {
    this.getMySurveys();
  }

  getMySurveys() {
      fetch('/api/surveys/my')
      .then(res => res.json())
      .then(data => {
          this.setState({surveys: data.sort((a: any, b: any) => (Date.parse(b.date) - Date.parse(a.date)))});
      });
  }

  addSurvey = (survey: Models.Survey) => {
    this.setState(state => {
      const surveys = [survey, ...state.surveys];
      return ({surveys});
    });
  }

  render(): JSX.Element {
    return(
      <>
        <div className="title-div">
          <h1 className="survey-title">Create new survey</h1>
        </div>
        <SurveyCreation addSurvey={this.addSurvey}/>
        <SurveyList surveys={this.state.surveys}/>
      </>
    );
  }
}
