import React, { Component } from 'react';
import { NavLink } from 'react-router-dom'
import Statistiques from './Statistiques';
import moment from 'moment'
import { connect } from 'react-redux'
import {formValueSelector} from 'redux-form'

let id = 'toto'

let filter_members = (members) => {
    var people = [];
    for (const key of Object.keys(members)) {
        if (members[key].status === 'success') {
            people.push(members[key]);
        }       
    }
    return people;
}

const dossierComplet = (eleve) => eleve.fiche_adhesion && eleve.certificat_medical && eleve.photo;

const renderEleve = (eleve, idx) =>
  <NavLink to={'/inscriptions/'+ eleve.id} className="nav-link" activeClassName="active">
    <li key={idx}>
      <i className={dossierComplet(eleve) ? "icon-check bg-success" : "icon-bell bg-warning"}></i>
      <div className="desc">
        <div className="title">{eleve.prenom} {eleve.nom}</div>
        <small>{eleve.surnom}</small>
      </div>
      <div
        className="actions"
        style={{
          marginTop: 10 + 'px'
        }}>
      </div>
    </li>
  </NavLink>


class Dashboard extends Component {
  render() {
    const { members = [] } = this.props;
    return (
      <div className="container">
        <div className="row">
          <div className="col">
            <div className="card bg-primary">
              <div className="card-block">
                <NavLink to={'/inscriptions'} className="nav-link text-white" activeClassName="active">
                  <h3>
                    <i className="fa fa-flag" style={{ marginRight: 10 + 'px' }} ></i>
                    Inscriptions</h3>
                </NavLink>
              </div>
            </div>
          </div>
          <div className="col">
            <div className="card bg-success">
              <div className="card-block">
                <NavLink to={'/appel/' + moment().format('YYYY-MM-DD')} className="nav-link text-white" activeClassName="active">
                  <h3>
                    <i className="fa fa-hand-paper-o" style={{ marginRight: 10 + 'px' }} ></i>
                    Faire l'appel</h3>
                </NavLink>
              </div>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <div className="card">
              <div className="card-block">
                {/* <NavLink to={'/inscriptions/'+id} className="nav-link text-white" activeClassName="active"> */}
                  <h3>
                    <i className="fa fa-edit" style={{ marginRight: 10 + 'px' }} ></i>
                    Modifier inscription pré-existante</h3>
                {/* </NavLink> */}
              </div>
              <div className="card-block" style={{marginTop: 0+'px'}}>
                  <div className="col-md-12" id="InscriptionsPreExistantes">
                      <ul className="icons-list">
                        <input
                        className="form-control"
                        type="search"
                        placeholder="Chercher nom"
                        id="example-search-input"/>
                        {filter_members(members).map(renderEleve)}
                      </ul>
                  </div>
              </div>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <Statistiques />
          </div>
        </div>
      </div>
    )
  }
}

const selector = formValueSelector('inscriptions')
Dashboard = connect(
    state => {
        return {
            members: state.membres
        }
    }
)(Dashboard)

export default Dashboard;
