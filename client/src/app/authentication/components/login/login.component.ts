import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Store } from '@ngrx/store';

import * as actions from '../../state/auth.actions';
import { selectAuthMessages } from '../../state/auth.selectors';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup = this.fb.group({
    'email': ['', [Validators.required, Validators.email]],
    'password': ['', Validators.required]
  })

  messages$ = this.store.select(selectAuthMessages);
  constructor(private fb: FormBuilder, private store: Store) { }

  ngOnInit(): void {
  }

  handleSubmit() {
    console.log(this.loginForm.value);
    this.store.dispatch(actions.login({body: this.loginForm.value}));
  }

  get email() {
    return this.loginForm.get('email') as AbstractControl;
  }

  get password() {
    return this.loginForm.get('password') as AbstractControl;
  }

}
