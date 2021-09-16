import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MainEffects } from './main/state/effects';
import { mainReducer } from './main/state/reducer';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    StoreModule.forRoot({
      main: mainReducer
    }, {}),
    EffectsModule.forRoot([MainEffects])
  ],
  providers: [
    { provide: 'API_URL', useValue: 'http://localhost:5000' },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
