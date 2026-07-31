import http from 'k6/http';
import { check } from 'k6';

const baseUrl = __ENV.BASE_URL || 'http://localhost:8000';

export const options = {
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
  scenarios: {
    health_20_tps: {
      executor: 'constant-arrival-rate',
      rate: 20,
      timeUnit: '1s',
      duration: '60s',
      preAllocatedVUs: 10,
      maxVUs: 50,
      tags: { load_stage: '20_tps' },
    },
    health_40_tps: {
      executor: 'constant-arrival-rate',
      startTime: '60s',
      rate: 40,
      timeUnit: '1s',
      duration: '60s',
      preAllocatedVUs: 20,
      maxVUs: 50,
      tags: { load_stage: '40_tps' },
    },
    health_80_tps: {
      executor: 'constant-arrival-rate',
      startTime: '120s',
      rate: 80,
      timeUnit: '1s',
      duration: '60s',
      preAllocatedVUs: 40,
      maxVUs: 100,
      tags: { load_stage: '80_tps' },
    },
    health_100_tps: {
      executor: 'constant-arrival-rate',
      startTime: '180s',
      rate: 100,
      timeUnit: '1s',
      duration: '60s',
      preAllocatedVUs: 50,
      maxVUs: 100,
      tags: { load_stage: '100_tps' },
    },
  },
  thresholds: {
    checks: ['rate==1'],
    http_req_failed: ['rate==0'],
    dropped_iterations: ['count==0'],
  },
};

export default function () {
  const response = http.get(`${baseUrl}/healthz`, {
    tags: { endpoint: 'healthz' },
  });

  check(response, {
    'status is 200': (res) => res.status === 200,
    'body reports healthy': (res) => res.json('ok') === true,
  });
}
